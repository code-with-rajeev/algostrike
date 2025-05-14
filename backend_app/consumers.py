import json
import asyncio
from channels.generic.websocket import AsyncWebsocketConsumer
from redis.asyncio import Redis

# StrategyConsumer is a tested and functional WebSocket consumer that handles real-time updates for a specific strategy.
# It connects to a Redis server, subscribes to a channel based on the strategy ID (`strategy_<StrategyID>`), and broadcasts messages to connected clients.
class StrategyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Extract the strategy ID from the URL
        self.strategy_id = self.scope["url_route"]["kwargs"]["strategy_id"]
        self.group_name = f"strategy_{self.strategy_id}"

        # Add this WebSocket connection to the group
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        # Initialize async Redis client
        self.redis_client = Redis.from_url("redis://localhost")
        self.redis_sub = self.redis_client.pubsub()
        await self.redis_sub.subscribe(self.group_name)

        # Send initial connection message
        await self.send(json.dumps({"status": "connected", "strategy_id": self.strategy_id}))

        # Start live updates in the background
        self.running = True
        self.update_task = asyncio.create_task(self.live_updates())

    async def disconnect(self, close_code):
        # Stop the update task
        self.running = False
        if hasattr(self, "update_task"):
            self.update_task.cancel()

        # Unsubscribe and close Redis connection
        await self.redis_sub.unsubscribe(self.group_name)
        await self.redis_client.close()

        # Remove from channel layer group
        await self.send(json.dumps({"status": "disconnected", "strategy_id": self.strategy_id}))        
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        # print("You sent to server", text_data)
        pass

    async def send_update(self, message):
        print("send", message)
        await self.send(json.dumps(message))

    async def live_updates(self):
        # Continuously listen for updates from Redis
        try:
            async for message in self.redis_sub.listen():
                if not self.running:
                    break
                if message["type"] == "message":
                    data = json.loads(message["data"].decode("utf-8"))
                    await self.send_update(data)
        except asyncio.CancelledError:
            pass  # Handle task cancellation gracefully
        except Exception as e:
            print(f"Error in live_updates: {e}")
        finally:
            await self.redis_sub.unsubscribe(self.group_name)

    async def on_start(self):
        print("Live data sending")
        await self.live_updates()  # This is now handled as a background task in connect