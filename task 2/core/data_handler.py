# core/data_handler.py

import streamlit as st
import pandas as pd
from datetime import datetime

# Define the name of the Google Sheet and Worksheet
SHEET_TITLE = "FyndFeedbackSubmissions"
WORKSHEET_NAME = "Submissions"


# Use Streamlit's built-in GSheets connector
# The connection is cached and managed by Streamlit
@st.cache_resource
def get_connection():
    # This looks for the secret file named .streamlit/secrets.toml
    return st.connection("gsheets", type="streamlit-gsheets")

def initialize_data_file():
    """
    Initializes the Google Sheet connection resource.
    """
    # Store the connection in session state for easy access in save_submission
    st.session_state["gsheets_conn"] = get_connection()
    # Attempt a read to ensure the connection is initialized upon startup
    try:
        st.session_state["gsheets_conn"].read(worksheet=WORKSHEET_NAME, ttl=0)
    except Exception as e:
        # This will happen if the sheet doesn't exist yet, which is fine
        print(f"GSheets initialization status: {e}") 
    

def save_submission(data: dict):
    """
    Appends a new submission (as a dictionary) to the Google Sheet.
    """
    conn = st.session_state.get("gsheets_conn")
    if not conn:
        st.error("GSheets connection not initialized. Cannot save data.")
        return

    # Convert the dictionary to a DataFrame for appending
    df_new_row = pd.DataFrame([data])
    
    # Append the row to the specified worksheet
    # The 'headers=True' ensures headers are written only on the first run
    conn.append(
        data=df_new_row, 
        worksheet=WORKSHEET_NAME,
        headers=True
    )
    # Clear the cache for the admin dashboard to see the new data immediately
    st.cache_data.clear()

def load_all_data() -> pd.DataFrame:
    """
    Reads all data from the Google Sheet for the Admin Dashboard.
    """
    conn = get_connection()
    try:
        # Use a short TTL (Time To Live) to frequently refresh the data
        df = conn.read(worksheet=WORKSHEET_NAME, ttl=1)
        # Ensure column headers are processed if the sheet is empty
        if df.empty:
            return pd.DataFrame(columns=df.columns)
        return df
    except Exception as e:
        # Return empty DataFrame if the sheet/worksheet is not found or empty
        print(f"Error loading data from GSheets: {e}")
        return pd.DataFrame()

# NOTE: The original load_all_submissions is replaced by load_all_data
