"""
This file serves as the entry point for the backend application. 
It initializes all the necessary configurations, starts required processes, 
and runs the core backend logic.

Note: Ensure the environment is set up (dependencies, Python path) before running this.
"""

import os
import sys

# Add the some folders to the Python path for module imports
# ROOT DIRECTORY
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Added some packages
# that may be needed for backend development

# Backend DIR
sys.path.append(os.path.join(ROOT_DIR, 'backend'))

# kotak_neo_api SDK DIR
sys.path.append(os.path.join(ROOT_DIR, 'kotak_neo'))


from settings import prod  # Import production settings
from core.scheduler import start_scheduler  # Example: Start a task scheduler
from algos.algo_router import route_algo  # Example: Main algo routing logic


def main():
    # 1. Set up the environment (logging, configs, etc.)
    print("Initializing Backend...")
    
    # Example: Check if required dependencies are installed (optional)
    try:
        import requests  # Example dependency
    except ImportError:
        print("Error: Required dependencies are missing. Install them via 'pip install -r requirements.txt'")
        sys.exit(1)
    
    # 2. Initialize logging or other settings
    print(f"Running in environment: {prod.ENVIRONMENT}")
    
    # 3. Start services or processes
    print("Starting Scheduler...")
    start_scheduler()  # Start the scheduler for background tasks
    
    # 4. Run core backend logic
    print("Running Algorithms...")
    route_algo()  # Route algorithms based on data/configs
    
    print("Backend Initialized Successfully")


if __name__ == "__main__":
    main()
