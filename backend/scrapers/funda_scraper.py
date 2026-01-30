from funda import Funda
from funda import Listing
import json
# TODO: remove max_budget, makes more sense to filter after scraping
class FundaScraperService:
    def __init__(self, area: str = None, want_to: str = "rent", n_pages: int = 2, max_budget: int = 1250, sort_by: str = "newest"):
        """
        Initialize the FundaScraper with search parameters.
        want_to: 'rent' for rent or 'buy' for buy.
        """
        self.scraper = Funda()
        self.area = area
        self.want_to = want_to
        self.n_pages = n_pages
        self.max_budget = max_budget
        self.sort_by = sort_by

    def scrape(self):
        """
        Runs the scraper and returns a list of dictionaries.
        """
        all_results = []
        for n in range(0, self.n_pages):
            # Funda-scraper's search_listing returns a list of Listing objects
            listings = self.scraper.search_listing(
                offering_type=self.want_to,
                price_max=self.max_budget,
                sort=self.sort_by,
                page=n,
                location=self.area,
            )
            
            for listing in listings:
                # get all listing details
                details = self.scraper.get_listing(listing.listing_id).to_dict()
                
                # Standardized core fields
                location = details.get('city', '')
                
                # Consolidate extra info (everything not in core)
                core_keys = {'title', 'price', 'url', 'photos', 'latitude', 'longitude'}
                extra = {k: v for k, v in details.items() if k not in core_keys}

                result = {
                    "title": details.get('title'),
                    "price": details.get('price'),
                    "location": location,
                    "link": details.get('url'),
                    "source": "Funda",
                    "type": self.want_to,
                    "media": details.get('photos'),
                    "extra": extra
                }
                
                # Add lat/lon directly if available
                if 'latitude' in details and 'longitude' in details:
                    result['lat'] = details['latitude']
                    result['lon'] = details['longitude']
                
                all_results.append(result)
                
        return all_results

if __name__ == "__main__":
    # Test run
    scraper = FundaScraperService(area="amsterdam", want_to="rent", n_pages=1, max_budget=2000)
    data = scraper.scrape()
    print(f"Scraped {len(data)} results from Funda.")
    print(data)
