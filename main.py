from fastapi import FastAPI, HTTPException, status, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from datetime import datetime
import re
from database import db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def is_valid_youtube_id(video_id):
    """Validate YouTube video ID format"""
    return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))

@app.on_event("startup")
async def startup_db_client():
    """Create indexes on startup"""
    await db.create_indexes()

@app.post("/api/videos")
async def add_video(request: Request):
    """Add a new YouTube video"""
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
        
        video_doc = {
            "videoId": video_id,
            "blocked": blocked,
            "addedAt": datetime.utcnow(),
            "addedBy": added_by,
            "updatedAt": datetime.utcnow()
        }
        
        if await db.video_exists(video_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Video already exists"
            )
        
        await db.add_video(video_doc)
        video_doc["_id"] = str(video_doc.get("_id", ""))
        
        return video_doc
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@app.get("/api/videos/{video_id}")
async def get_video(video_id: str):
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
async def get_stats():
    """Get statistics"""
    return await db.get_stats()

@app.put("/api/videos/{video_id}")
async def update_video_status(video_id: str, request: Request):
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
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
