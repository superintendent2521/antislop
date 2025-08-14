# YouTube Blocker API - Complete Endpoint Documentation

## Base URL
`http://localhost:8000`

## All API Endpoints

### 1. Health Check
```
GET /
```
**Response:**
```json
{"status": "ok", "service": "youtube-block-api"}
```

---

### 2. Add New Video
```
POST /api/videos
Content-Type: application/json
```

**Request Body:**
```json
{
    "videoId": "dQw4w9WgXcQ",
    "blocked": true,
    "addedBy": "admin"
}
```

**Required Fields:**
- `videoId`: string (11-character YouTube video ID)
- `blocked`: boolean (true/false)
- `addedBy`: string (username/identifier of who added it)

**Response (201 Created):**
```json
{
    "videoId": "dQw4w9WgXcQ",
    "blocked": true,
    "addedAt": "2025-08-14T00:35:00.123Z",
    "addedBy": "admin",
    "updatedAt": "2025-08-14T00:35:00.123Z",
    "_id": "64b7f8e9a1b2c3d4e5f6g7h8"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid YouTube video ID or missing required fields
- `409 Conflict`: Video already exists

---

### 3. Check Video Status (Anonymous)
```
GET /api/videos/{video_id}
```

**URL Parameters:**
- `video_id`: string (11-character YouTube video ID)

**Response (200 OK):**
```json
{
    "videoId": "dQw4w9WgXcQ",
    "blocked": true
}
```

**Error Responses:**
- `400 Bad Request`: Invalid YouTube video ID format
- `404 Not Found`: Video not found

---

### 4. Get Statistics
```
GET /api/stats
```

**Response (200 OK):**
```json
{
    "totalVideos": 42,
    "totalBlocked": 15
}
```

---

### 5. Update Video Status
```
PUT /api/videos/{video_id}
Content-Type: application/json
```

**URL Parameters:**
- `video_id`: string (11-character YouTube video ID)

**Request Body:**
```json
{
    "blocked": false
}
```

**Required Fields:**
- `blocked`: boolean (true/false)

**Response (200 OK):**
```json
{
    "videoId": "dQw4w9WgXcQ",
    "blocked": false,
    "addedAt": "2025-08-14T00:30:00.000Z",
    "addedBy": "admin",
    "updatedAt": "2025-08-14T00:35:00.000Z",
    "_id": "64b7f8e9a1b2c3d4e5f6g7h8"
}
```

**Error Responses:**
- `400 Bad Request`: Invalid YouTube video ID or missing blocked field
- `404 Not Found`: Video not found

---

## YouTube Video ID Format
- Must be exactly 11 characters
- Allowed characters: letters (a-z, A-Z), numbers (0-9), underscore (_), hyphen (-)
- Examples: `dQw4w9WgXcQ`, `jNQXAC9IVRw`, `kJQP7kiw5Fk`

## Testing Examples

### Add a video:
```bash
curl -X POST http://localhost:8000/api/videos \
  -H "Content-Type: application/json" \
  -d '{"videoId":"dQw4w9WgXcQ","blocked":true,"addedBy":"admin"}'
```

### Check if blocked (anonymous):
```bash
curl http://localhost:8000/api/videos/dQw4w9WgXcQ
```

### Get stats:
```bash
curl http://localhost:8000/api/stats
```

### Update status:
```bash
curl -X PUT http://localhost:8000/api/videos/dQw4w9WgXcQ \
  -H "Content-Type: application/json" \
  -d '{"blocked":false}'
