import streamlit as st
import pandas as pd
from datetime import datetime

# Import the core service files
try:
    from core.data_handler import initialize_data_file, save_submission 
    from core.llm_service import LLMService, StructuredOutput
    
    # Initialize LLM Service and Data Storage
    llm_service = LLMService()
    initialize_data_file() # Ensure the CSV is ready on startup
except ImportError as e:
    # Fallback 
    st.error(f"Error initializing core services (LLM/Data). Check your 'core' directory setup. Error: {e}")
   
    class MockLLMService:
        def __init__(self): pass
        def generate_structured_response(self, r, rv):
            from dataclasses import dataclass
            @dataclass
            class MockStructuredOutput:
                user_response: str
                admin_summary: str
                admin_actions: str
            
            if r >= 4: 
                return MockStructuredOutput(
                    user_response="Thank you so much! We're thrilled to hear you enjoyed your experience. (Mock)",
                    admin_summary="Mock Summary.",
                    admin_actions="Mock Action 1, Mock Action 2, Mock Action 3"
                )
            return MockStructuredOutput(
                user_response="Thank you for your feedback. We appreciate your input for improvement. (Mock)",
                admin_summary="Mock Summary.",
                admin_actions="Mock Action 1, Mock Action 2, Mock Action 3"
            )
    llm_service = MockLLMService()
    def save_submission(data): pass


# Config 
st.set_page_config(
    page_title="Feedback",
    layout="centered",
    initial_sidebar_state="collapsed"
)


st.markdown(
    """
    <style>
    /* 1. Global Font and Compactness */
    body {
        /* Clean San Serif font stack */
        font-family: ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
    }
    .stApp > header {visibility: hidden;}
    div.stPageLink { display: none; }
    
    
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 600px;
    }
    
    
    .stApp > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) > div:nth-child(1) {
        text-align: center;
    }

    
    .stButton>button {
        width: 100%;
        max-width: 200px; 
        border-radius: 999px; /* Pill shape */
        padding: 10px 20px;
        font-weight: 600;
        /* Custom Blue Color */
        background-color: #0070f0; 
        border: 1px solid #0070f0;
        color: white; 
    }
    .stButton>button:hover {
        background-color: #005bb5; 
        border: 1px solid #005bb5;
    }
    
    
    .stInfo {
        border-radius: 8px;
        text-align: left;
        font-size: 1.05em;
        line-height: 1.5;
    }
    h2 {
        margin-top: 0.5em !important;
        margin-bottom: 0.2em !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


#UI Layout


st.markdown("<h1 style='font-weight: 500;'>Feedback</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-top:-10px; margin-bottom: 40px; color: #555555; font-size: 1.1em;'>Your input helps us improve.</p>", unsafe_allow_html=True)

with st.form(key='feedback_form'):
    
    #Rating Input
    st.markdown("<h3 style='margin-bottom: 10px; font-weight: 500;'>Rate your satisfaction</h3>", unsafe_allow_html=True)

    star_rating = st.slider(
        "Rating",
        min_value=1,
        max_value=5,
        value=3,
        step=1,
        format="%d ⭐",
        label_visibility="collapsed"
    )
    
    st.markdown("---") 

    #Review Text Area ---
    st.markdown("<h3 style='margin-bottom: 10px; font-weight: 500;'>Share your experience</h3>", unsafe_allow_html=True)
    review_text = st.text_area(
        "Your Review:", 
        placeholder="What was great? What could be better?", 
        max_chars=500,
        label_visibility="collapsed"
    )

    #Submit Button 
    col_L, col_C, col_R = st.columns([1, 1, 1])
    with col_C:
        submitted = st.form_submit_button("Submit", type="primary")

# submission Logic and AI Response Display
if submitted:
    if not review_text:
        st.error("Please provide a comment before submitting.")
    else:
        
        with st.spinner('Analyzing feedback and generating response...'):
            
         
            structured_output = llm_service.generate_structured_response(star_rating, review_text)
            
            # Unpack the structured output for use in the dashboard and saving
            user_response = structured_output.user_response
            ai_summary = structured_output.admin_summary
            ai_actions = structured_output.admin_actions

            # Store Data
            submission_data = {
                "timestamp": datetime.now().isoformat(),
                "user_rating": star_rating,
                "user_review": review_text,
                "ai_user_response": user_response,
                "ai_summary": ai_summary, 
                "ai_actions": ai_actions
            }
            save_submission(submission_data)

            
        # Display AI Response
        st.info(user_response)
        st.markdown("-----")

