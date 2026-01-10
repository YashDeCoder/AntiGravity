import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "antigravity_db")

async def check_db():
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    count = await db.houses.count_documents({})
    print(f"Total houses in DB: {count}")
    
    if count > 0:
        sample = await db.houses.find_one()
        print(f"Sample house source: {sample.get('source')}")
        print(f"Sample house price: {sample.get('price')}")
        print(f"Sample house travel_data: {sample.get('travel_data')}")

if __name__ == "__main__":
    asyncio.run(check_db())
