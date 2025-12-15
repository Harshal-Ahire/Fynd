import streamlit as st
import pandas as pd
from datetime import datetime

from core.data_handler import load_all_submissions

# --- Configuration & Setup ---
st.set_page_config(
    page_title="Feedback Admin Dashboard",
    layout="wide", # Use wide layout for better table viewing
    initial_sidebar_state="collapsed"
)

# Custom CSS for a clean, professional admin look
st.markdown(
    """
    <style>
    /* 1. Global Layout and Styling */
    .block-container {
        padding-top: 2rem;
    }
    h1 {
        font-weight: 600;
        color: #0070f0; 
        text-align: left !important; /* Ensure the title is left-aligned */
    }
    h2, h3, h4, h5, h6 {
        text-align: left;
    }

    /* 2. Metric Box Styling */
    .metric-box {
        padding: 20px;
        border-radius: 8px;
        background-color: #f0f2f6; 
        border: 1px solid #e0e0e0;
        text-align: center;
        margin-bottom: 20px;
    }
    .metric-value {
        font-size: 2.5em;
        font-weight: 700;
        color: #333333;
    }
    .metric-label {
        font-size: 1.1em;
        color: #555555;
        margin-top: 5px;
    }
    
    /* 3. Streamlit Dataframe Centering (Need to wrap in a centered container below) */
    .stDataFrame {
        margin-left: auto;
        margin-right: auto;
    }
    </style>
    """,
    unsafe_allow_html=True
)


@st.cache_data(ttl=1) 
def load_data():
    """Loads and preprocesses the feedback data from Google Sheets."""
    
    # Load data from Google Sheets via data handler
    df = load_all_submissions()

    if df.empty:
        return df

    # 1. Convert timestamp to datetime and format Date
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    # Format the Date column as requested: 15 Dec, 2025
    df['Date'] = df['timestamp'].dt.strftime('%d %b, %Y')
    
    # 2. Create the formatted Rating column (e.g., "5 ★★★★★")
    # FIX: Use .apply() to safely perform element-wise string repetition
    def star_formatter(rating):
        return str(rating) + ' ' + ('★' * rating)

    df['Rating'] = df['user_rating'].apply(star_formatter)

    # 3. Rename columns for display
    df.rename(columns={
        'user_review': 'Customer Review',
        'ai_user_response': 'AI Response',
        'ai_summary': 'AI Summary (Internal)',
        'ai_actions': 'AI Actions (Internal)'
    }, inplace=True)

    # Reorder columns for the main table display
    df = df[['Date', 'Rating', 'Customer Review', 'AI Response', 'AI Summary (Internal)', 'AI Actions (Internal)', 'user_rating']]
    
    return df

# UI Layout
st.title("Admin Dashboard")
st.markdown("Monitor and analyze user feedback with AI-powered insights.")
st.markdown("---")

df_data = load_data()

if df_data.empty:
    st.info("No feedback submissions have been recorded yet.")
else:
    
    header_col, button_col, status_col = st.columns([4, 2, 3])

    with header_col:
        st.markdown("## Key Performance Indicators")
    
    with button_col:
        # The button now forces a clear cache and rerun to get fresh data
        if st.button("Refresh Data", type="primary", use_container_width=True):
            st.cache_data.clear() # Clears the cache to force a fresh Google Sheets read
            st.rerun() # Reruns the script to fetch new data
            st.toast("Data refreshed!")
            
    with status_col:
        
        current_time = datetime.now().strftime("%H:%M:%S")
        st.caption(f"Last UI refresh: {current_time}")

    
    col1, col2, col3, col_spacer = st.columns([1, 1, 1, 3]) # Metrics columns

    with col1:
        avg_rating = df_data['user_rating'].mean()
        avg_rating_formatted = f"{avg_rating:.1f}"
        st.markdown(f"""
        <div class="metric-box">
            <div class="metric-value">{avg_rating_formatted}</div>
            <div class="metric-label">Average Star Rating</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.metric(label="Total Submissions", value=len(df_data))
        
    with col3:
        positive_count = df_data[df_data['user_rating'] >= 4].shape[0]
        st.metric(label="Positive Reviews (4★/5★)", value=positive_count)

    st.markdown("---")

    # Filter Control
    st.markdown("## Review Submissions")
    
    min_rating = st.slider(
        'Minimum Star Rating to Display',
        min_value=1, max_value=5, value=1
    )
    
    filtered_df = df_data[df_data['user_rating'] >= min_rating]


    # Create columns to push the table 
    col_left, col_center, col_right = st.columns([1, 5, 1]) 
    
    display_columns = ['Date', 'Rating', 'Customer Review', 'AI Response']

    with col_center:
        st.dataframe(
            filtered_df[display_columns], 
            use_container_width=True, 
            hide_index=True
        )

    #Detailed Internal AI Data 
    with st.expander("Show Internal AI Summaries and Actions"):
        st.dataframe(
            filtered_df[['Date', 'user_rating', 'AI Summary (Internal)', 'AI Actions (Internal)']], 
            use_container_width=True,
            hide_index=True
        )
