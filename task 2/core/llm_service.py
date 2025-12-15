# Imports

import os
from dataclasses import dataclass
from groq import Groq, APIStatusError

# API Key Configuration
GROQ_API_KEY = os.getenv("GROQ_API_KEY") 
GROQ_MODEL = 'llama-3.1-8b-instant'  # Groq model


# Structured Output Dataclass
@dataclass
class StructuredOutput:
    """Container for all three outputs from a single API call."""
    user_response: str
    admin_summary: str
    admin_actions: str


class LLMService:
    """Handles all interactions with the Large Language Model for Task 2."""
    def __init__(self):
       
        print("GROQ_API_KEY loaded:", bool(GROQ_API_KEY)) 
        
        if not GROQ_API_KEY:
            print("WARNING: LLMService is using mock data. GROQ_API_KEY not found in .env or environment.")
            self.client = None
        else:
            try:
                # Initialize the Groq client
                self.client = Groq(api_key=GROQ_API_KEY)
            except Exception as e:
                print(f"Error initializing Groq client: {e}")
                self.client = None

        self.model = GROQ_MODEL

    # --- CONSOLIDATED METHOD USING STRUCTURED OUTPUT ---
    def generate_structured_response(self, rating: int, review: str) -> StructuredOutput:
        """
        Generates all three required outputs (User Response, Summary, Actions) 
        in a single API call using Groq's JSON mode for efficiency.
        """
        import json  # Local import needed for parsing

        prompt = f"""
        You are a powerful AI assistant analyzing user feedback. 
        Your task is to provide three distinct outputs based on the Star Rating ({rating}) and User Review ("{review}").
        
        1. **User Response (user_response):** Act as a polite, human customer service agent. The response must be 30-60 words, acknowledge the review, and be suitable for public display. Do NOT mention internal actions.
        
        2. **Admin Summary (admin_summary):** Summarize the review into one concise sentence (max 15 words) for quick managerial review.
        
        3. **Admin Actions (admin_actions):** Generate 3 specific, actionable recommendations for a manager. Format these as a single, comma-separated string (e.g., "Action 1, Action 2, Action 3").
        
        Format your final output STRICTLY as a JSON object with the keys: user_response, admin_summary, and admin_actions.
        """
        
        if self.client:
            try:
                response = self.client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=self.model,
                    response_format={"type": "json_object"} 
                )
                
                json_text = response.choices[0].message.content
                parsed_json = json.loads(json_text)
                
                return StructuredOutput(
                    user_response=parsed_json.get('user_response', "Error: Response missing."),
                    admin_summary=parsed_json.get('admin_summary', "Error: Summary missing."),
                    admin_actions=parsed_json.get('admin_actions', "Error: Actions missing.")
                )
                
            except APIStatusError as e:
                print(f"Groq API Status Error ({e.status_code}): {e.message}")
            except Exception as e:
                print(f"Groq Client Error: {e}")
        
        # --- FALLBACK (MOCK DATA) ---
        if rating >= 4:
            return StructuredOutput(
                user_response="Thank you for your excellent feedback! (MOCK)",
                admin_summary="Positive review highlighting excellent service. (MOCK)",
                admin_actions="Send team feedback, Use review for marketing, Monitor similar future reviews (MOCK)"
            )
        else:
            return StructuredOutput(
                user_response="We sincerely apologize for your experience. We are addressing this. (MOCK)",
                admin_summary="Negative review citing customer support issues. (MOCK)",
                admin_actions="Immediate manager follow-up, Identify root cause, Update training materials (MOCK)"

            )
