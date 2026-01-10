from scrapers.funda_scraper import FundaScraperService  
from scrapers.pararius import ParariusScraperService
from scrapers.verhuurtbeter import VerhuurtbeterScraperService
from distance_service import get_travel_data, geocode_address
from database import get_database
import asyncio

class HousingService:
    def __init__(self):
        self.db = get_database()

    async def run_all_scrapers(self, city: str):
        """
        Runs all scrapers, calculates travel data, and saves to DB.
        """
        scrapers = [
            FundaScraperService(want_to="rent"),
            FundaScraperService(want_to="buy", max_budget=225000),
            # ParariusScraperService(city=city),
            # VerhuurtbeterScraperService()
        ]
        
        all_results = []
        
        for s in scrapers:
            try:
                # Running scrapers in separate threads to avoid blocking event loop
                results = await asyncio.to_thread(s.scrape)
                all_results.extend(results)
            except Exception as e:
                print(f"Error running scraper {s.__class__.__name__}: {e}")

        # Process results: Check distance and save to DB
        processed_count = 0
        for house in all_results:
            # Basic deduplication based on link
            existing = await self.db.houses.find_one({"link": house["link"]})
            if existing:
                continue
            
            # Geocode if coordinates are missing
            if "lat" not in house or "lon" not in house:
                address = f"{house['title']}, {house['location']}"
                coords = await asyncio.to_thread(geocode_address, address)
                if coords:
                    house["lat"] = coords["lat"]
                    house["lon"] = coords["lon"]
            
            # Calculate travel info if coordinates exist
            if "lat" in house and "lon" in house:
                travel_info = await asyncio.to_thread(get_travel_data, house["lat"], house["lon"])
                if travel_info and "error" not in travel_info:
                    house["travel_data"] = travel_info
            
            await self.db.houses.insert_one(house)
            processed_count += 1
            
        return {"scraped": len(all_results), "new": processed_count}

    async def get_filtered_houses(self, max_budget: int = None, max_duration: float = None):
        """
        Retrieves houses from DB with filtering.
        """
        query = {}
        if max_budget:
            query["price"] = {"$lte": max_budget}
            
        houses = await self.db.houses.find(query).to_list(100)
        
        # In-memory duration filtering if it's not indexed/stored in a way that Mongo likes
        if max_duration:
            houses = [h for h in houses if h.get("travel_data", {}).get("duration_mins", 999) <= max_duration]
            
        for h in houses:
            h["_id"] = str(h["_id"])
            
        return houses
