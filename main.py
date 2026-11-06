from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.security import verify_admin
from backend.vapi_service import VapiService
from backend.assistant_service import AssistantService
from backend.call_service import CallService
from backend.webhook_service import WebhookService

app = FastAPI(title="DIY AI Voice Calling Agent Platform", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Vapi AI Voice Agent Backend"}

@app.get("/api/config/status")
def config_status():
    return {
        "vapi_phone": settings.VAPI_PHONE_NUMBER,
        "phone_number_id": settings.VAPI_PHONE_NUMBER_ID,
        "model": settings.OPENROUTER_MODEL,
        "firebase_project": settings.FIREBASE_PROJECT_ID
    }

@app.get("/api/assistants")
def get_assistants(admin=Depends(verify_admin)):
    return AssistantService.get_all_assistants()

@app.post("/api/assistants")
async def create_assistant(request: Request, admin=Depends(verify_admin)):
    data = await request.json()
    name = data.get("name", "AI Assistant")
    system_prompt = data.get("system_prompt", "You are a helpful AI assistant speaking in Hindi and English.")
    first_message = data.get("first_message", "Hello! How can I help you today?")
    
    # We construct a dynamic webhook URL based on the request host
    base_url = str(request.base_url).rstrip("/")
    server_url = f"{base_url}/api/vapi/webhook"

    # Create in Vapi
    vapi_res = VapiService.create_assistant(name, system_prompt, first_message, server_url)
    assistant_id = vapi_res.get("id")

    # Automatically assign to phone number
    try:
        VapiService.assign_phone_number(settings.VAPI_PHONE_NUMBER_ID, assistant_id, server_url)
    except Exception as e:
        print(f"Warning during phone assignment: {e}")

    # Save to Firebase DB
    db_record = {
        "assistant_id": assistant_id,
        "name": name,
        "system_prompt": system_prompt,
        "first_message": first_message,
        "server_url": server_url
    }
    AssistantService.save_assistant_to_db(db_record)

    return {"status": "success", "assistant": db_record}

@app.get("/api/calls")
def get_calls(admin=Depends(verify_admin)):
    return CallService.get_call_logs()

@app.post("/api/vapi/webhook")
async def vapi_webhook(request: Request):
    payload = await request.json()
    return WebhookService.handle_vapi_event(payload)
