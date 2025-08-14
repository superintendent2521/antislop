from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

class Database:
    def __init__(self):
        self.client = AsyncIOMotorClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
        self.db = self.client[os.getenv("DATABASE_NAME", "youtube_blocker")]
        self.videos = self.db["videos"]

    async def create_indexes(self):
        await self.videos.create_index("videoId", unique=True)

    async def add_video(self, video_data):
        result = await self.videos.insert_one(video_data)
        return result.inserted_id

    async def get_video(self, video_id):
        return await self.videos.find_one({"videoId": video_id})

    async def update_video_status(self, video_id, blocked):
        result = await self.videos.update_one(
            {"videoId": video_id},
            {"$set": {"blocked": blocked, "updatedAt": "datetime.utcnow()"}}
        )
        return result.modified_count

    async def get_stats(self):
        total = await self.videos.count_documents({})
        blocked = await self.videos.count_documents({"blocked": True})
        return {"totalVideos": total, "totalBlocked": blocked}

    async def video_exists(self, video_id):
        return await self.videos.find_one({"videoId": video_id}) is not None

db = Database()
