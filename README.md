# YouTube Video Blocker API

A simple FastAPI-based service for tracking blocked YouTube videos with MongoDB.

## Features
- Add YouTube videos with blocking status
- Check if a video is blocked (anonymous response)
- Get statistics on total videos and blocked videos
- Update video blocking status

## Requirements
- Python 3.7+
- MongoDB
- FastAPI

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Start MongoDB locally or update `.env` with your MongoDB URI

3. Run the server:
```bash
python main.py
```

## API Endpoints

### Add a video
```bash
POST /api/videos
Content-Type: application/json

{
    "videoId": "dQw4w9WgXcQ",
    "blocked": true,
    "addedBy": "admin"
}
```

### Check if video is blocked (anonymous)
```bash
GET /api/videos/dQw4w9WgXcQ
```

### Get statistics
```bash
GET /api/stats
```

### Update video status
```bash
PUT /api/videos/dQw4w9WgXcQ
Content-Type: application/json

{
    "blocked": false
}
```

## Data Model
- **videoId**: YouTube video ID (11 characters)
- **blocked**: Boolean indicating if video is blocked
- **addedAt**: Timestamp when added
- **addedBy**: User who added the video (internal tracking)
- **updatedAt**: Last modification time

## Anonymous Responses
When checking if a video is blocked, the API only returns:
```json
{
    "videoId": "dQw4w9WgXcQ",
    "blocked": true
}
```
No user information is exposed, besides required things (if it doesnt have it, it wont work!) Like: Useragent and ip. 
