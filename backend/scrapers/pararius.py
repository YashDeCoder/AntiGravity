import requests
from bs4 import BeautifulSoup
import re

class ParariusScraperService:
    def __init__(self, city: str = "amsterdam"):
        self.city = city.lower()
        self.base_url = f"https://www.pararius.nl/huurwoningen/{self.city}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scrape(self):
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            
            listings = []
            cards = soup.select(".listing-search-item")
            
            for card in cards:
                title_elem = card.select_one(".listing-search-item__title")
                price_elem = card.select_one(".listing-search-item__price")
                location_elem = card.select_one(".listing-search-item__sub-title")
                link_elem = card.select_one("a.listing-search-item__link--title")
                
                if not title_elem or not price_elem:
                    continue
                    
                title = title_elem.get_text(strip=True)
                price_text = price_elem.get_text(strip=True)
                location = location_elem.get_text(strip=True) if location_elem else ""
                link = "https://www.pararius.nl" + link_elem["href"] if link_elem else ""
                
                # Clean price: extract digits
                price = re.sub(r"[^\d]", "", price_text)
                
                listings.append({
                    "title": title,
                    "price": int(price) if price else 0,
                    "location": location,
                    "link": link,
                    "source": "Pararius",
                    "type": "rent", # Pararius is primarily rent
                    "media": [],    # Could be enhanced to scrape thumbnails
                    "extra": {
                        "price_text": price_text
                    }
                })
                
            return listings
        except Exception as e:
            print(f"Error scraping Pararius: {e}")
            return []

if __name__ == "__main__":
    scraper = ParariusScraperService(city="amsterdam")
    data = scraper.scrape()
    print(f"Scraped {len(data)} results from Pararius.")
    if data:
        for item in data[:3]:
            print(item)
