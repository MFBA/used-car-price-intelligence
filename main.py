import argparse
from scraper import PakWheelsScraper
from cleaner import clean_dataset

def main():
    parser = argparse.ArgumentParser(description="PakWheels Scraper MVP")
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to scrape")
    parser.add_argument("--output", type=str, default="scraped_data", help="Output filename base (without extension)")
    
    args = parser.parse_args()
    
    print(f"Starting scraper for {args.pages} pages...")
    
    scraper = PakWheelsScraper()
    df = scraper.scrape_listings(max_pages=args.pages)

    
    if not df.empty:
        print(f"Scraped {len(df)} listings.")
        
        # Clean the data
        print("Cleaning data...")
        cleaned_df = clean_dataset(df)
        print(cleaned_df.head())
        print(cleaned_df.info())
        
        # Save raw data
        scraper.save_to_csv(df, f"{args.output}_raw.csv")
        
        # Save cleaned data
        scraper.save_to_csv(cleaned_df, f"{args.output}_cleaned.csv")
        scraper.save_to_json(cleaned_df, f"{args.output}_cleaned.json")
    else:
        print("No data scraped.")

if __name__ == "__main__":
    main()
