class Settings:
    # Vapi Configuration
    VAPI_PRIVATE_API_KEY: str = "YOUR_VAPI_PRIVATE_API_KEY_HERE"  # Paste your Vapi Private API Key from Vapi Dashboard
    VAPI_PHONE_NUMBER_ID: str = "7ab46ffd-9452-4c4b-ad24-20143add8043"
    VAPI_PHONE_NUMBER: str = "+15312130113"

    # OpenRouter Configuration
    OPENROUTER_API_KEY: str = "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"
    OPENROUTER_MODEL: str = "nvidia/nemotron-3.5-super-vl:free"

    # Deepgram Configuration
    DEEPGRAM_API_KEY: str = "bf41dd319bb54a8cf20d3185507eaab1308bb268"

    # Firebase Realtime Database Configuration
    FIREBASE_DATABASE_URL: str = "https://commutrade-default-rtdb.firebaseio.com"
    FIREBASE_PROJECT_ID: str = "commutrade"
    FIREBASE_CREDENTIALS_PATH: str = None  # Uses default app or web config if needed

    # CORS / Frontend
    FRONTEND_ORIGIN: str = "*"

settings = Settings()
