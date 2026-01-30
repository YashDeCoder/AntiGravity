import requests
import json
import re

class VestedaScraperService:
    def __init__(self):
        self.api_url = "https://www.vesteda.com/api/units/search/facet"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept": "application/json, text/plain, */*",
            "Content-Type": "application/json",
            "Referer": "https://www.vesteda.com/nl/woning-zoeken",
        }

    def scrape(self, filter: bool = True):
        try:
            payload = {
                "placeType": 0,
                "sortType": 1,
                "radius": 20,
                "s": "",
                "sc": "woning",
                "latitude": 0,
                "longitude": 0,
                "filters": [],
                "priceFrom": 500,
                "priceTo": 9999
            }
            
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            data = response.json()
            
            listings = []
            objects = data.get("results", {}).get("objects", [])
            
            for obj in objects:
                if filter:
                    # Filter out unavailable houses
                    status = obj.get("status")
                    status_text = obj.get("statusText", "").lower()
                    
                    # Exclude if status is not 1 (Available) or status_text indicates it's taken
                    if status is not None and status != 1:
                        continue
                    if any(keyword in status_text for keyword in ["gereserveerd", "verhuurd", "voorbehoud"]):
                        continue

                title = f"{obj.get('street', '')} {obj.get('houseNumber', '')}"
                if obj.get('houseNumberAddition'):
                    title += f" {obj.get('houseNumberAddition')}"
                
                price = obj.get("priceUnformatted", 0)
                # If priceUnformatted is missing, try to parse from price string
                if not price:
                    price_str = obj.get("price", "0")
                    price_match = re.search(r"(\d+)", price_str.replace(".", "").replace(",", ""))
                    price = int(price_match.group(1)) if price_match else 0

                link = obj.get("url", "")
                if link and not link.startswith("http"):
                    link = "https://www.vesteda.com" + link

                media = []
                if obj.get("imageBig"):
                    media.append(obj.get("imageBig"))

                listings.append({
                    "title": title.strip(),
                    "price": int(price),
                    "location": obj.get("city", ""),
                    "link": link,
                    "type": "rent",
                    "media": media,
                    "source": "Vesteda",
                    "extra": {
                        "size": obj.get("size"),
                        "rooms": obj.get("numberOfBedRooms"),
                        "property_type": obj.get("entitysubtypelabel"),
                        "district": obj.get("district"),
                        "postalCode": obj.get("postalCode")
                    }
                })
                
            return listings
        except Exception as e:
            print(f"Error scraping Vesteda: {e}")
            return []

if __name__ == "__main__":
    scraper = VestedaScraperService()
    data = scraper.scrape()
    print(f"Scraped {len(data)} results from Vesteda.")
    if data:
        for item in data[:3]:
            print(json.dumps(item, indent=2))