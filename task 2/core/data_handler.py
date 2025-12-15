import pandas as pd
import os

DATA_FILE = "submissions.csv"

def initialize_data_file():
    """Checks if the data file exists and creates it with headers if not."""
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "timestamp",
            "user_rating",
            "user_review",
            "ai_user_response",
            "ai_summary",
            "ai_actions" # Storing the comma separated string 
        ])
        df.to_csv(DATA_FILE, index=False)
        print(f"Created new data file: {DATA_FILE}")

def save_submission(data: dict):
    """Appends a new submission dictionary to the CSV file."""
    # Ensure the columns match the order 
    new_data = {key: [data.get(key, '')] for key in [
        "timestamp", 
        "user_rating", 
        "user_review", 
        "ai_user_response", 
        "ai_summary", 
        "ai_actions"
    ]}
    
    new_row_df = pd.DataFrame(new_data)
    
    # Append to the CSV file
    new_row_df.to_csv(DATA_FILE, mode='a', header=False, index=False)

def load_all_submissions():
    """Loads all submission data for the Admin Dashboard."""
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame() # Return empty DataFrame if file doesn't exist