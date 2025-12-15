# core/data_handler.py

import streamlit as st
import pandas as pd
from datetime import datetime
import os
import json
import gspread
from google.oauth2.service_account import Credentials

# Define the name of the Google Sheet and Worksheet
SHEET_TITLE = "FyndFeedbackSubmissions"
WORKSHEET_NAME = "Submissions"

# Define the required scopes for Google Sheets API
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

@st.cache_resource
def get_sheet():
    """
    Establishes connection to Google Sheets using gspread and service account credentials.
    Returns the worksheet object for data operations.
    """
    try:
        # Load credentials from ENV VAR (Render-compatible)
        credentials_dict = json.loads(
            os.environ["STREAMLIT_SECRETS_GCP_SERVICE_ACCOUNT"]
        )

        # Create credentials object
        credentials = Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
        
        # Authorize gspread client
        client = gspread.authorize(credentials)
        
        # Open the spreadsheet and get the worksheet
        spreadsheet = client.open(SHEET_TITLE)
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        
        return worksheet
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {e}")
        return None


def initialize_data_file():
    """
    Initializes the Google Sheet by ensuring the header row exists.
    If the sheet is empty, it adds the column headers.
    """
    try:
        sheet = get_sheet()
        if sheet is None:
            return
        
        # Check if the sheet has any data
        all_values = sheet.get_all_values()
        
        # If empty, add headers
        if len(all_values) == 0:
            headers = [
                "timestamp",
                "user_rating",
                "user_review",
                "ai_user_response",
                "ai_summary",
                "ai_actions"
            ]
            sheet.append_row(headers)
            print(f"Initialized Google Sheet '{SHEET_TITLE}' with headers")
    except Exception as e:
        print(f"Error initializing Google Sheet: {e}")


def save_submission(data: dict):
    """
    Appends a new submission (as a dictionary) to the Google Sheet.
    """
    try:
        sheet = get_sheet()
        if sheet is None:
            st.error("Could not connect to Google Sheets. Submission not saved.")
            return
        
        # Ensure the data is in the correct order matching the headers
        row_data = [
            data.get("timestamp", ""),
            data.get("user_rating", ""),
            data.get("user_review", ""),
            data.get("ai_user_response", ""),
            data.get("ai_summary", ""),
            data.get("ai_actions", "")
        ]
        
        # Append the row to the sheet
        sheet.append_row(row_data)
        
    except Exception as e:
        st.error(f"Error saving submission to Google Sheets: {e}")


def load_all_submissions():
    """
    Loads all submission data from the Google Sheet for the Admin Dashboard.
    Returns a pandas DataFrame.
    """
    try:
        sheet = get_sheet()
        if sheet is None:
            return pd.DataFrame()
        
        # Get all records as a list of dictionaries
        records = sheet.get_all_records()
        
        # Convert to DataFrame
        if len(records) == 0:
            # Return empty DataFrame with expected columns if no data
            return pd.DataFrame(columns=[
                "timestamp",
                "user_rating",
                "user_review",
                "ai_user_response",
                "ai_summary",
                "ai_actions"
            ])
        
        df = pd.DataFrame(records)
        return df
        
    except Exception as e:
        print(f"Error loading data from Google Sheets: {e}")
        return pd.DataFrame()
