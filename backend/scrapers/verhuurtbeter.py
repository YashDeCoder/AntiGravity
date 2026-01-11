import requests
from bs4 import BeautifulSoup
import re

class VerhuurtbeterScraperService:
    def __init__(self):
        self.base_url = "https://verhuurtbeter.nl/aanbod"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    def scrape(self):
        try:
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, "html.parser")
            
            listings = []
            cards = soup.select(".object-item")
            
            for card in cards:
                price_elem = card.select_one(".f-rentalprice")
                address_elems = card.select(".f-address")
                
                if not price_elem or not address_elems:
                    continue
                
                # Title is usually the first address element's link text
                title_link = address_elems[0].find("a")
                title = title_link.get_text(strip=True) if title_link else address_elems[0].get_text(strip=True)
                
                # Location is usually the second address element's link text
                location = ""
                if len(address_elems) > 1:
                    location_link = address_elems[1].find("a")
                    location = location_link.get_text(strip=True) if location_link else address_elems[1].get_text(strip=True)
                
                price_text = price_elem.get_text(strip=True)
                # Clean price: extract digits
                price = re.sub(r"[^\d]", "", price_text.split(',')[0]) # Handle decimal with comma
                
                link = ""
                if title_link:
                    link = title_link["href"]
                    if not link.startswith("http"):
                        link = "https://verhuurtbeter.nl" + link

                media = []
                img_elem = card.select_one(".object-thumb img")
                if img_elem and img_elem.get("src"):
                    media = [img_elem["src"]]

                listings.append({
                    "title": title,
                    "price": int(price) if price else 0,
                    "location": location,
                    "link": link,
                    "type": "rent",
                    "media": media,
                    "source": "Verhuurtbeter",
                    "extra": {
                        "price_text": price_text
                    }
                })
                
            return listings
        except Exception as e:
            print(f"Error scraping Verhuurtbeter: {e}")
            return []

if __name__ == "__main__":
    scraper = VerhuurtbeterScraperService()
    data = scraper.scrape()
    print(f"Scraped {len(data)} results from Verhuurtbeter.")
    if data:
        for item in data[:3]:
            print(item)
