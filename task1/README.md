# Task 1: LLM-Based Rating Prediction

This task evaluates different **LLM prompting strategies** for predicting **Yelp review star ratings (1–5)**.  
The objective is to compare prompt effectiveness using structured outputs and quantitative evaluation metrics.

All implementation, experiments, and analysis for Task 1 are contained in a **single Jupyter Notebook**.

---

## Problem Overview
Given a text-based user review, the system predicts an overall star rating using a Large Language Model.  
The focus is on prompt design, output consistency, and performance comparison rather than model fine-tuning.

---

## Dataset
- Yelp Reviews dataset (Kaggle)
- 200 stratified samples
- Multiclass classification (1–5 stars)

---

## Prompting Strategies Evaluated
1. **Zero-Shot Prompting**  
   Direct classification with minimal instruction, relying on the model’s inherent understanding of sentiment.

2. **Few-Shot Prompting**  
   Uses representative examples (positive, neutral, negative) to guide rating decisions.

3. **Chain-of-Verification (CoV)**  
   A multi-step reasoning approach where the model analyzes sentiment, assigns a provisional rating, verifies consistency, and produces a final output.

---

## LLM Configuration
- Model: Google Gemini 2.0 Flash  
- Structured output enforced using Pydantic schema validation  

---

## Evaluation Metrics
Each prompting strategy is evaluated using:
- Accuracy
- Precision (Macro)
- Recall (Macro)
- F1-Score (Macro)
- Output validity rate
- Average inference time

---

## Results Summary
The **Zero-Shot prompting strategy** achieved the best overall performance, offering a strong balance of accuracy, reliability, and low latency across the evaluation dataset.

---

## Tech Stack
- Python
- Google Gemini API
- Pydantic
- pandas
- scikit-learn

---

## How to Run
```bash
jupyter notebook Task1_LLM_Evaluation.ipynb
