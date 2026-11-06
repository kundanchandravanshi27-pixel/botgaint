import requests
from backend.config import settings

class VapiService:
    BASE_URL = "https://api.vapi.ai"

    @classmethod
    def _get_headers(cls):
        return {
            "Authorization": f"Bearer {settings.VAPI_PRIVATE_API_KEY}",
            "Content-Type": "application/json"
        }

    @classmethod
    def create_assistant(cls, name: str, system_prompt: str, first_message: str, server_url: str):
        url = f"{cls.BASE_URL}/assistant"
        payload = {
            "name": name,
            "firstMessage": first_message,
            "model": {
                "provider": "openrouter",
                "model": settings.OPENROUTER_MODEL,
                "apiKey": settings.OPENROUTER_API_KEY,
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    }
                ]
            },
            "transcriber": {
                "provider": "deepgram",
                "model": "nova-2",
                "language": "multi",
                "apiKey": settings.DEEPGRAM_API_KEY
            },
            "voice": {
                "provider": "deepgram",
                "voiceId": "aura-asteria-en"
            },
            "serverUrl": server_url
        }
        response = requests.post(url, json=payload, headers=cls._get_headers())
        if response.status_code not in [200, 201]:
            raise Exception(f"Vapi API Error: {response.text}")
        return response.json()

    @classmethod
    def update_assistant(cls, assistant_id: str, payload: dict):
        url = f"{cls.BASE_URL}/assistant/{assistant_id}"
        response = requests.patch(url, json=payload, headers=cls._get_headers())
        if response.status_code != 200:
            raise Exception(f"Vapi Update Error: {response.text}")
        return response.json()

    @classmethod
    def assign_phone_number(cls, phone_number_id: str, assistant_id: str, server_url: str):
        url = f"{cls.BASE_URL}/phone-number/{phone_number_id}"
        payload = {
            "assistantId": assistant_id,
            "serverUrl": server_url
        }
        response = requests.patch(url, json=payload, headers=cls._get_headers())
        if response.status_code != 200:
            raise Exception(f"Vapi Phone Assignment Error: {response.text}")
        return response.json()
