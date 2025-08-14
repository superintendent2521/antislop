import json
import os
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

def load_keys():
    """Load API keys from keys.json"""
    try:
        with open('keys.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API keys configuration not found"
        )

def get_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Extract and validate API key from Authorization header"""
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header required"
        )
    
    token = credentials.credentials
    if not token.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization format. Use 'Bearer <api-key>'"
        )
    
    api_key = token.replace("Bearer ", "")
    return api_key

def require_api_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Require and validate API key against master key"""
    api_key = get_api_key(credentials)
    
    keys = load_keys()
    master_key = keys.get("master_key")
    
    if not master_key:
        print("No masterkey!")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal error. report to developer with timeframe"
        )
    
    if api_key != master_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return api_key
