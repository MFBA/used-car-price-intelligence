import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

class PakWheelsScraper:
    def __init__(self, base_url="https://www.pakwheels.com/used-cars/search/-/"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def fetch_page(self, url):
        """Fetches a single page and returns the BeautifulSoup object"""
        try:
            print(f"Fetching: {url}")
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.text, 'html.parser')
        except requests.RequestException as e:
            print(f"Error fetching {url}: {e}")
            return None

    def parse_listing(self, listing_soup):
        """Extracts details from a single card"""
        try:
            title_tag = listing_soup.find('a', class_='car-name')
            name = title_tag.get_text(strip=True) if title_tag else "N/A"
            listing_url = "https://www.pakwheels.com" + title_tag['href'] if title_tag and title_tag.has_attr('href') else "N/A"

            price_tag = listing_soup.find(class_='price-details')
            price = price_tag.get_text(strip=True) if price_tag else "N/A"

            city_ul = listing_soup.find('ul', class_='search-vehicle-info')
            city = city_ul.find('li').get_text(strip=True) if city_ul and city_ul.find('li') else "N/A"

            details_ul = listing_soup.find('ul', class_='search-vehicle-info-2')
            details = {}
            if details_ul:
                lis = details_ul.find_all('li')
                if len(lis) >= 1: details['year'] = lis[0].get_text(strip=True)
                if len(lis) >= 2: details['mileage'] = lis[1].get_text(strip=True)
                if len(lis) >= 3: details['fuel'] = lis[2].get_text(strip=True)
                if len(lis) >= 4: details['engine'] = lis[3].get_text(strip=True)
                if len(lis) >= 5: details['transmission'] = lis[4].get_text(strip=True)

            return {
                'name': name,
                'price': price,
                'url': listing_url,
                'city': city,
                **details
            }
        except Exception as e:
            print(f"Error parsing listing: {e}")
            return None

    def scrape_listings(self, max_pages=1):
        """Main loop to scrape listings across multiple pages"""
        all_listings = []
        
        for page in range(1, max_pages + 1):
            url = f"{self.base_url}?page={page}"
            soup = self.fetch_page(url)
            
            if not soup:
                continue

            listings = soup.find_all('li', class_='classified-listing')
            
            if not listings:
                print("No listings found on page. Selectors might need adjustment.")
                break

            print(f"Found {len(listings)} listings on page {page}")

            for listing in listings:
                data = self.parse_listing(listing)
                if data:
                    all_listings.append(data)
            
            time.sleep(random.uniform(1, 3))

        return pd.DataFrame(all_listings)

    def save_to_csv(self, df, filename="scraped_data.csv"):
        df.to_csv(filename, index=False)
        print(f"Saved to {filename}")

    def save_to_json(self, df, filename="scraped_data.json"):
        df.to_json(filename, orient='records', indent=4)
        print(f"Saved to {filename}")
