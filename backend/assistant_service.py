from backend.firebase_service import FirebaseService
from backend.vapi_service import VapiService

class AssistantService:
    @staticmethod
    def save_assistant_to_db(assistant_data: dict):
        ref = FirebaseService.get_ref("assistants")
        new_ref = ref.push()
        assistant_data["id"] = new_ref.key
        new_ref.set(assistant_data)
        return assistant_data

    @staticmethod
    def get_all_assistants():
        ref = FirebaseService.get_ref("assistants")
        data = ref.get()
        if not data:
            return []
        return list(data.values())

    @staticmethod
    def get_assistant(assistant_id: str):
        ref = FirebaseService.get_ref(f"assistants/{assistant_id}")
        return ref.get()
