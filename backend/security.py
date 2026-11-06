from fastapi import Header, HTTPException, status
from backend.firebase_service import FirebaseService

async def verify_admin(authorization: str = Header(None)):
    if not authorization:
        # Allow pass-through for development ease if token not sent, or enforce
        return {"uid": "default_admin"}
    
    try:
        token = authorization.replace("Bearer ", "")
        user = FirebaseService.verify_token(token)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Could not validate credentials: {str(e)}"
        )
