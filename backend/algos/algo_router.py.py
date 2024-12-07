"""
NOTE: This code is for demonstration purposes only. It is not functional as-is 
and is designed to showcase maintainability, modularity, and workflow interactions.
"""

from algos.algo1.decision_logic import generate_signal as algo1_signal
from algos.algo2.decision_logic import generate_signal as algo2_signal
from shared.premarket_analysis import analyze_premarket
from shared.data_fetcher import get_live_data
from core.notification import send_notification

# Define routing logic for algorithms
def route_algo(index, algo_name):
    """
    Route the task to the appropriate algorithm based on its name.
    """
    if algo_name == "algo1":
        return algo1_signal(index)
    elif algo_name == "algo2":
        return algo2_signal(index)
    else:
        raise ValueError(f"Unknown algorithm: {algo_name}")

def execute_algorithms():
    """
    Main function to execute all registered algorithms for the day.
    """
    # Step 1: Analyze premarket data to decide indices to monitor
    indices = analyze_premarket()
    active_algorithms = ["algo1", "algo2"]  # Example: active algorithms today

    # Step 2: Loop through indices and execute each algorithm
    for index in indices:
        for algo_name in active_algorithms:
            try:
                # Fetch live data for the index
                live_data = get_live_data(index)

                # Generate and validate signal for the algorithm
                signal = route_algo(index, algo_name)
                if signal:
                    # Send notification for valid signal
                    send_notification(algo_name, index, signal)
                    print(f"Signal generated by {algo_name} for {index}: {signal}")

            except Exception as e:
                print(f"Error in {algo_name} for {index}: {str(e)}")

# Example standalone execution
if __name__ == "__main__":
    execute_algorithms()