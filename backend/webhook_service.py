from backend.call_service import CallService

class WebhookService:
    @staticmethod
    def handle_vapi_event(payload: dict):
        event_type = payload.get("message", {}).get("type")
        call_data = payload.get("message", {}).get("call", {})
        
        call_id = call_data.get("id", "unknown_call")
        status = call_data.get("status", event_type)
        customer = call_data.get("customer", {}).get("number", "Unknown")
        transcript = payload.get("message", {}).get("transcript", "")
        summary = payload.get("message", {}).get("summary", "")

        log_payload = {
            "call_id": call_id,
            "customer_phone": customer,
            "status": status,
            "transcript": transcript,
            "summary": summary,
            "direction": call_data.get("type", "inbound")
        }
        
        CallService.log_call(log_payload)
        return {"status": "received"}
