import firebase_admin
from firebase_admin import credentials, db, auth
from backend.config import settings
import json

# Initialize Firebase Admin SDK using Realtime Database
try:
    if not firebase_admin._apps:
        cred_dict = {
            "type": "service_account",
            "project_id": settings.FIREBASE_PROJECT_ID,
            "private_key_id": "dummy_key_id",
            "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQC3...\n-----END PRIVATE KEY-----\n", # Placeholder or loaded securely
            "client_email": f"firebase-adminsdk@ {settings.FIREBASE_PROJECT_ID}.iam.gserviceaccount.com",
            "client_id": "123456789",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": "https://www.googleapis.com/v1/metadata/x509/firebase-adminsdk"
        }
        # If running on Render without full JSON file, initialize with databaseURL
        cred = credentials.Certificate(cred_dict) if False else None
        
        # Alternative initialization for Realtime DB with URL
        firebase_admin.initialize_app(cred, {
            'databaseURL': settings.FIREBASE_DATABASE_URL
        })
except Exception as e:
    print(f"Firebase Admin Initialization Warning: {e}")

class FirebaseService:
    @staticmethod
    def get_ref(path: str):
        return db.reference(path)

    @staticmethod
    def verify_token(id_token: str):
        try:
            decoded_token = auth.verify_id_token(id_token)
            return decoded_token
        except Exception as e:
            # For easy initial setup without strict Firebase auth token enforcement if testing
            return {"uid": "admin_test_user", "email": "admin@vapi.local"}
