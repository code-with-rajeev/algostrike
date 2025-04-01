from celery import shared_task
from myapp.models import Algo  # Adjust your ORM model
from backend.interfaces.cache_manager import CacheManager
#from backend.core.uttils import get_logger

#logger = get_logger('app')

"""
ABOUT: handles the entire process of fetching data asynchronously by creating threads.
Types of Streams:
    - SUB:
        subscribe to websocket stream and get realtime ticks.
        difficult to manage and raises connenction lost problem.
        needed to re-connent many time.
    - SNAP:
        Uses session token of user to fetch current tick at that instant.
        Fast but need to process and manage OHLC data.
    - API:
        Uses broker's public to fetch OHLC data in date range.
        This process is delayed but accurate.
        One time fetching at specific range(recommended).
"""

from celery import shared_task
from celery.schedules import crontab
from myapp.models import Algo
from backend.interfaces.cache_manager import CacheManager
import threading
import time
from datetime import datetime
import json
import asyncio
from typing import Dict, Optional
#import logging

logger = logging.getLogger('app')

class Snap:
    def __init__(self):
        self.key = 'active_algos:algo:requirements:SNAP'
        self.cache = CacheManager()
        self.tasks = {}  # {instrument: {timeframe, task_id, last_fetch}}
        self.lock = threading.Lock()
        self.default_timeframe = "1M"
        self.token = ""  # Should be set via config or auth method
        self.running = False
        self.data_fetcher = None  # Should be injected via dependency injection

    @shared_task(bind=True)
    async def create_task(self, task_data: Dict) -> str:
        """Create a periodic task for data fetching"""
        try:
            instrument = task_data['instrument']
            timeframe = task_data.get('timeframe', self.default_timeframe)
            
            # Store task metadata in Redis
            task_id = f"snap_task_{instrument}_{int(time.time())}"
            task_metadata = {
                'instrument': instrument,
                'timeframe': timeframe,
                'task_id': task_id,
                'created_at': datetime.utcnow().isoformat()
            }
            
            with self.lock:
                self.tasks[instrument] = task_metadata
                await self.cache.hset(self.key, instrument, json.dumps(task_metadata))
            
            logger.info(f"Created task for {instrument} with timeframe {timeframe}")
            return task_id
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            raise

    async def add_snap(self, new_task: Dict) -> bool:
        """Add a new instrument to monitor"""
        try:
            instrument = new_task['instrument']
            timeframe = new_task.get('timeframe', self.default_timeframe)
            
            if instrument in self.tasks:
                logger.warning(f"Instrument {instrument} already exists")
                return False
                
            task_data = {'instrument': instrument, 'timeframe': timeframe}
            await self.create_task(task_data)
            return True
        except Exception as e:
            logger.error(f"Error adding snap: {str(e)}")
            return False

    async def remove_snap(self, instrument: str):
        """Remove an instrument from monitoring"""
        try:
            with self.lock:
                if instrument in self.tasks:
                    task_data = self.tasks.pop(instrument)
                    await self.cache.hdel(self.key, instrument)
                    logger.info(f"Removed snap for {instrument}")
                    return True
            return False
        except Exception as e:
            logger.error(f"Error removing snap: {str(e)}")
            return False

    async def fetch_once(self, instrument: str):
        """Fetch current data ticks once"""
        try:
            if not self.data_fetcher:
                raise ValueError("Data fetcher not initialized")
                
            data = await self.data_fetcher.fetch(instrument, token=self.token)
            await self.cache.set(f"snap_data:{instrument}", json.dumps(data), ex=300)  # 5 min TTL
            return data
        except Exception as e:
            logger.error(f"Error fetching data for {instrument}: {str(e)}")
            return None

    @shared_task(bind=True)
    async def trigger_task(self):
        """Periodic task to fetch data for all instruments"""
        try:
            if not self.tasks:
                return
                
            async with asyncio.Lock():  # Async lock for concurrent safety
                tasks = list(self.tasks.items())
                for instrument, metadata in tasks:
                    data = await self.fetch_once(instrument)
                    if data:
                        # Process OHLC data based on timeframe if needed
                        await self._process_timeframe_data(instrument, metadata['timeframe'], data)
        except Exception as e:
            #logger.error(f"Error in trigger task: {str(e)}")


    async def start_snap(self):
        """Initialize snap service from Redis"""
        try:
            if self.running:
                return
                
            self.running = True
            cached_data = await self.cache.hgetall(self.key)
            
            async with asyncio.Lock():
                for instrument, task_json in cached_data.items():
                    task_data = json.loads(task_json)
                    self.tasks[instrument] = task_data
                    
            # Schedule periodic task
            from celery import current_app
            current_app.add_periodic_task(
                crontab(minute='*/1'),  # Every minute
                self.trigger_task.s(),
                name='snap_data_fetcher'
            )
            #logger.info("Snap service started")
        except Exception as e:
            #logger.error(f"Error starting snap: {str(e)}")
            self.running = False

    async def stop_snap(self):
        """Gracefully stop the snap service"""
        self.running = False
        with self.lock:
            self.tasks.clear()
        await self.cache.delete(self.key)


class StreamSubscriber:
    def __init__(self):
        self.cache = CacheManager()
        self.snap_handler = Snap()

    async def subscribe(self, mode, task):
        """Subscribe to a streaming mode"""
        try:
            if mode == "SNAP":
                return await self.snap_mode(task)
            # Add SUB and API modes when implemented
            return False
        except Exception as e:
            #logger.error(f"Error in subscribe: {str(e)}")
            return False

    async def snap_mode(self, task):
        """Handle SNAP mode subscription"""
        return await self.snap_handler.add_snap(task)
