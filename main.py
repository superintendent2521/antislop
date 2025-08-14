from fastapi import FastAPI, HTTPException, status, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import re
import os
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from database import db
from auth import get_api_key, require_api_key

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

# Configure CORS with specific allowed origins
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080").split(",")
allowed_origins = [origin.strip() for origin in allowed_origins if origin.strip()]

# Allow all origins in development
if os.getenv("ENVIRONMENT") == "development":
    allowed_origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

def is_valid_youtube_id(video_id):
    """Validate YouTube video ID format"""
    return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))

@app.on_event("startup")
async def startup_db_client():
    """Create indexes on startup"""
    await db.create_indexes()

@app.post("/api/videos")
@limiter.limit("10/minute")
async def add_video(request: Request):
    """Add a new YouTube video, or return the existing one if already added."""
    try:
        data = await request.json()
        
        video_id = data.get("videoId")
        if not video_id or not is_valid_youtube_id(video_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid YouTube video ID"
            )
        
        added_by = data.get("addedBy")
        if not added_by:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="addedBy is required"
            )
        
        blocked = data.get("blocked", False)
        
        existing = await db.get_video(video_id)
        if existing:
            existing["_id"] = str(existing["_id"])
            return {
                "message": "This video has already been added",
                "existing": existing
            }
        
        video_doc = {
            "videoId": video_id,
            "blocked": blocked,
            "addedAt": datetime.utcnow(),
            "addedBy": added_by,
            "updatedAt": datetime.utcnow()
        }
        
        inserted_id = await db.add_video(video_doc)
        video_doc["_id"] = str(inserted_id)
        return video_doc
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
@app.get("/api/videos/{video_id}")
@limiter.limit("30/minute")
async def get_video(video_id: str, request: Request):
    """Get a video by ID - anonymous response"""
    if not is_valid_youtube_id(video_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid YouTube video ID"
        )
    
    video = await db.get_video(video_id)
    if not video:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"blocked": False}
        )
    # Return anonymous response
    return {
        "videoId": video["videoId"],
        "blocked": video["blocked"]
    }

@app.get("/api/stats")
@limiter.limit("20/minute")
async def get_stats(request: Request):
    """Get statistics"""
    return await db.get_stats()

@app.put("/api/videos/{video_id}")
@limiter.limit("5/minute")
async def update_video_status(video_id: str, request: Request, api_key: str = Depends(require_api_key)):
    """Update video blocked status"""
    try:
        if not is_valid_youtube_id(video_id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid YouTube video ID"
            )
        
        data = await request.json()
        blocked = data.get("blocked")
        if blocked is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="blocked field is required"
            )
        #above prevents querying the db for bogus requests, helps prevent load from misbehaving apps/and or bad actors
        modified = await db.update_video_status(video_id, blocked)
        if modified == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Video not found"
            )
        
        video = await db.get_video(video_id)
        video["_id"] = str(video["_id"])
        
        return video
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "service": "youtube-block-api"}

if __name__ == "__main__":
    import uvicorn
    import os
    if os.path.exists("fih.webp"):
        uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
    else:
        print("Fih needed ")
