from funda import Funda
from funda import Listing
import json

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
            list_listings = self.scraper.search_listing(
                offering_type=self.want_to,
                price_max=self.max_budget,
                sort=self.sort_by,
                page=n,
                location=self.area,
            )
            all_results.extend(list_listings)
        return all_results

if __name__ == "__main__":
    # Test run
    scraper = FundaScraperService(area="utrecht", want_to="rent", n_pages=2)
    data = scraper.scrape()
    print(f"Scraped {len(data)} results from Funda.")
    if data:
        for r in data:
            print(r['price'], r['location'])
