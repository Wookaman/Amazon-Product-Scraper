# main_scraper.py
from scraper_function import scraper

def main():
    url = input("Please enter the Amazon URL to scrape: ")
    amazon_df = scraper(url)

    print("\n>> Scraped Products:")
    print(amazon_df.head(10))
   # print("\n>> Price Stats:")
   # print(amazon_stats)

    filename = "amazon_data.csv"
    amazon_df.to_csv(filename, index=False)
    print(f"\n>> Data saved to {filename}")

if __name__ == "__main__":
    main()
