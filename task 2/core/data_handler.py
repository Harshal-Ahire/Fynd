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
        # Load the raw string from the environment variable
        json_string = os.environ.get("STREAMLIT_SECRETS_GCP_SERVICE_ACCOUNT")
        
        if not json_string:
            print("ERROR: STREAMLIT_SECRETS_GCP_SERVICE_ACCOUNT environment variable not found!")
            st.error("Environment variable STREAMLIT_SECRETS_GCP_SERVICE_ACCOUNT is missing")
            return None
        
        print(f"JSON string length: {len(json_string)}")
        print(f"JSON string starts with: {json_string[:50]}...")
        
        # Parse the JSON
        credentials_dict = json.loads(json_string.strip())
        print("✓ JSON parsed successfully")
        
        # Create credentials object
        credentials = Credentials.from_service_account_info(
            credentials_dict,
            scopes=SCOPES
        )
        print("✓ Credentials created successfully")
        
        # Authorize gspread client
        client = gspread.authorize(credentials)
        print("✓ Client authorized successfully")
        
        # Open the spreadsheet
        spreadsheet = client.open(SHEET_TITLE)
        print(f"✓ Spreadsheet '{SHEET_TITLE}' opened successfully")
        
        # Get the worksheet
        worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
        print(f"✓ Worksheet '{WORKSHEET_NAME}' accessed successfully")
        
        return worksheet
        
    except KeyError as e:
        error_msg = f"Missing environment variable: {e}"
        print(f"ERROR: {error_msg}")
        st.error(error_msg)
        return None
    except json.JSONDecodeError as e:
        error_msg = f"Invalid JSON in service account credentials: {e}"
        print(f"ERROR: {error_msg}")
        st.error(error_msg)
        return None
    except gspread.exceptions.SpreadsheetNotFound:
        error_msg = f"Spreadsheet '{SHEET_TITLE}' not found. Check the name and sharing permissions."
        print(f"ERROR: {error_msg}")
        st.error(error_msg)
        return None
    except gspread.exceptions.WorksheetNotFound:
        error_msg = f"Worksheet '{WORKSHEET_NAME}' not found in spreadsheet '{SHEET_TITLE}'."
        print(f"ERROR: {error_msg}")
        st.error(error_msg)
        return None
    except gspread.exceptions.APIError as e:
        error_msg = f"Google Sheets API Error: {e}"
        print(f"ERROR: {error_msg}")
        st.error(error_msg)
        return None
    except Exception as e:
        error_msg = f"Unexpected error connecting to Google Sheets: {type(e).__name__}: {e}"
        print(f"ERROR: {error_msg}")
        st.error(error_msg)
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
            # Displays the error message seen in the user's output
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
        print(f"✓ Successfully saved submission to Google Sheets")
        
    except Exception as e:
        error_msg = f"Error saving submission to Google Sheets: {e}"
        print(f"ERROR: {error_msg}")
        st.error(error_msg)


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
        print(f"✓ Successfully loaded {len(df)} submissions from Google Sheets")
        return df
        
    except Exception as e:
        print(f"Error loading data from Google Sheets: {e}")
        return pd.DataFrame()
