# AI-Powered Feedback System

This project is an AI-driven feedback system built using **Streamlit** and **Groq AI**.  
It collects user ratings and reviews, generates contextual AI responses, and provides an internal admin dashboard for analysis.

---

## Features

### User Dashboard
- Star rating system (1–5)
- Free-text customer feedback
- Context-aware AI-generated reply (powered by Groq's LLaMA models)
- Data stored automatically for analysis
- **Single API call optimization** using structured outputs

### Admin Dashboard
- View all feedback submissions
- Average rating and review metrics
- AI summaries and suggested actions
- Filter reviews by star rating
- **Real-time data refresh** with manual refresh button
- Last update timestamp display

---

## Tech Stack
- **Python 3.8+**
- **Streamlit** - Web interface
- **Groq API** - AI-powered response generation (LLaMA 3.1)
- **Pandas** - Data processing and analysis
- **python-dotenv** - Environment variable management

---

## Project Structure