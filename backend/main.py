from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from database import ping_db, get_database
from distance_service import get_travel_data
from housing_service import HousingService
import uvicorn
from typing import Optional

app = FastAPI(title="AntiGravity All-in-One App")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development, allow all. In production, restrict this.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

housing_service = HousingService()

@app.on_event("startup")
async def startup_db_client():
    await ping_db()

@app.get("/")
async def root():
    return {"message": "Welcome to AntiGravity API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/scrape")
async def trigger_scrape(city: str = "amsterdam"):
    result = await housing_service.run_all_scrapers(city=city)
    return result

@app.get("/houses")
async def get_houses(
    max_budget: Optional[int] = Query(None, description="Maximum monthly rent"),
    max_duration: Optional[float] = Query(None, description="Maximum travel duration in minutes"),
    source: Optional[str] = Query(None, description="Filter by listing source")
):
    houses = await housing_service.get_filtered_houses(
        max_budget=max_budget, 
        max_duration=max_duration,
        source=source
    )
    return houses

@app.post("/test-distance")
async def test_distance(lat: float, lon: float):
    result = get_travel_data(lat, lon)
    return result

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
