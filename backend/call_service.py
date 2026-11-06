from backend.firebase_service import FirebaseService
from datetime import datetime

class CallService:
    @staticmethod
    def log_call(call_data: dict):
        ref = FirebaseService.get_ref("call_logs")
        call_id = call_data.get("call_id", ref.push().key)
        call_data["timestamp"] = datetime.utcnow().isoformat()
        ref.child(call_id).set(call_data)
        return call_data

    @staticmethod
    def get_call_logs():
        ref = FirebaseService.get_ref("call_logs")
        data = ref.get()
        if not data:
            return []
        return list(data.values())
