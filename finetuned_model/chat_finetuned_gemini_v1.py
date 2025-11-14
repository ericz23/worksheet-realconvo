import os
import json
import requests
from google.oauth2 import service_account
from google.auth.transport.requests import Request
from dotenv import load_dotenv

# ==========================================================
# Finetuned Gemini Client
# ==========================================================
class FinetunedGeminiClient:
    def __init__(self):
        self.project_id = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
        self.region = os.getenv("VERTEX_AI_REGION")
        self.endpoint_id = os.getenv("VERTEX_AI_ENDPOINT_ID")
        self.credentials = self._setup_credentials()
        self.endpoint_url = self._build_endpoint_url()
        
        # persistent conversation context
        self.history = []

    def _setup_credentials(self):
        credentials_json_str = os.getenv("GOOGLE_APPLICATION_CREDENTIALS_JSON")
        credentials_info = json.loads(credentials_json_str)
        return service_account.Credentials.from_service_account_info(
            credentials_info,
            scopes=["https://www.googleapis.com/auth/cloud-platform"],
        )

    def _build_endpoint_url(self):
        return f"https://{self.region}-aiplatform.googleapis.com/v1/projects/{self.project_id}/locations/{self.region}/endpoints/{self.endpoint_id}:generateContent"

    def generate_content(self, prompt: str, temperature: float = 0.2, max_tokens: int = 10000) -> str:
        """Generate content using your finetuned Gemini model"""
        # Append new user message to history
        self.history.append({"role": "user", "parts": [{"text": prompt}]})

        payload = {
            "system_instruction": {
                "role": "system",
                "parts": [
                    {
                        "text": """
                        You are a helpful medical appointment scheduling customer agent. Follow professional call center etiquette and assist the customer 
                        in booking, rescheduling, or confirming appointments. Your task is to act as the 'Agent' in a conversation with a 'Customer'. 
                        Generate only the agent's responses, one turn at a time, to help the customer with their medical appointment needs.
                        """
                    }
                ]
            },
            "contents": self.history,
            "generation_config": {
                "temperature": temperature,
                "max_output_tokens": max_tokens,
            },
        }

        self.credentials.refresh(Request())
        headers = {
            "Authorization": f"Bearer {self.credentials.token}",
            "Content-Type": "application/json",
        }

        response = requests.post(self.endpoint_url, json=payload, headers=headers)

        if response.status_code == 200:
            response_data = response.json()
            try:
                model_reply = response_data["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                model_reply =  str(response_data)
        else:
            raise Exception(f"HTTP {response.status_code}: {response.text}")
        
        self.history.append({"role": "model", "parts": [{"text": model_reply}]})
        return model_reply


# ==========================================================
# Interactive chat
# ==========================================================
def main():
    print("Initializing Fine-tuned Gemini Client...")
    load_dotenv()

    client = FinetunedGeminiClient()
    print("Connected to fine-tuned Gemini model.\nType 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() in ["exit"]:
            print("Exiting chat.")
            break

        response = client.generate_content(user_input)
        print(f"Agent: {response}\n")


if __name__ == "__main__":
    main()