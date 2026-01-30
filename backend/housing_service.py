from scrapers.funda_scraper import FundaScraperService  
from scrapers.pararius import ParariusScraperService
from scrapers.verhuurtbeter import VerhuurtbeterScraperService
from scrapers.vesteda import VestedaScraperService
from distance_service import get_travel_data, geocode_address, get_closest_station
from database import get_database
import asyncio

class HousingService:
    def __init__(self):
        self.db = get_database()

    async def run_all_scrapers(self, target: str = "Hoekenrode 10A, 1101 DT Amsterdam", buy: bool = False):
        """
        Runs all scrapers, calculates travel data, and saves to DB.
        """
        # Resolve target station UIC code once
        dest_uic = None
        target_coords = await asyncio.to_thread(geocode_address, target)
        if target_coords:
            target_station = await asyncio.to_thread(get_closest_station, target_coords["lat"], target_coords["lon"])
            if "error" not in target_station:
                dest_uic = target_station["closest_station_uicCode"]
        
        scrapers = [
            FundaScraperService(want_to="rent"),
            # FundaScraperService(want_to="buy"),
            # ParariusScraperService(city=city),
            # VerhuurtbeterScraperService(),
            VestedaScraperService(),
        ]
        
        if buy:
            scrapers.append(FundaScraperService(want_to="buy", max_budget=225000))

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
                travel_info = await asyncio.to_thread(get_travel_data, house["lat"], house["lon"], dest_uic)
                if travel_info and "error" not in travel_info:
                    house["travel_data"] = travel_info
            
            await self.db.houses.insert_one(house)
            processed_count += 1
            
        return {"scraped": len(all_results), "new": processed_count}

    async def get_filtered_houses(self, max_budget: int = None, max_duration: float = None, source: str = None):
        """
        Retrieves houses from DB with filtering.
        """
        query = {}
        if max_budget:
            query["price"] = {"$lte": max_budget}
        
        if source and source.lower() != "all":
            # Using case-insensitive regex for source just in case
            query["source"] = source
            
        houses = await self.db.houses.find(query).to_list(100)
        
        # In-memory duration filtering: if travel_data is missing, we still show the house
        # unless it explicitly exceeds the duration.
        if max_duration:
            houses = [h for h in houses if int(h.get("travel_data").get("duration_minutes")) <= max_duration]
            
        for h in houses:
            h["_id"] = str(h["_id"])
            
        return houses
