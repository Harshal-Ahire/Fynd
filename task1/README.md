# Task 1: LLM-Based Rating Prediction

This task evaluates multiple LLM prompting strategies for predicting **Yelp review star ratings (1–5)** using structured outputs and quantitative metrics.  
All implementation and analysis are contained in a **single Jupyter Notebook**.

---

## Overview
- Dataset: Yelp Reviews (Kaggle), 200 stratified samples  
- Model: Google Gemini 2.0 Flash  
- Output: Strict JSON validated using Pydantic  

Each prediction returns:
```json
{
  "predicted_stars": 1-5,
  "explanation": "brief reasoning"
}
