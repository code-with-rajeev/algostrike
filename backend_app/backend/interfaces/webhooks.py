"""
NOTE: This code is for demonstration purposes only. It is designed to show
how to handle client requests and fetch order history in a modular way.
"""

from flask import Flask, request, jsonify
import database_helper  # A custom module for database operations

app = Flask(__name__)

@app.route('/client/order_history', methods=['GET'])
def get_order_history():
    """
    Handle the request to fetch order history for a client.
    """
    try:
        # Get the client ID from query parameters
        client_id = request.args.get('id')
        
        if not client_id:
            return jsonify({"error": "Client ID is required"}), 400

        # Validate client ID (basic validation, e.g., check if it's numeric)
        if not client_id.isdigit():
            return jsonify({"error": "Invalid Client ID"}), 400

        # Fetch order history from the database (pseudo-code)
        order_history = database_helper.fetch_order_history(client_id)
        
        # Check if data exists
        if not order_history:
            return jsonify({"error": "No order history found"}), 404

        # Return the order history
        return jsonify({"client_id": client_id, "order_history": order_history}), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error fetching order history: {str(e)}")
        return jsonify({"error": "Server error"}), 500

if __name__ == "__main__":
    app.run(port=5000)