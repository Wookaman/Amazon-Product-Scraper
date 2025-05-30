# Amazon-Product-Scraper

## About
The Amazon scraper is written in Python. It is a lightweight Amazon.ca product scraper, using the `BeautifulSoup` library alongside `Pandas` to effectively scrape all relevant product data given a user-inputted URL and create a `DataFrame`.

## Requirements
Install the required dependencies found in the `requirements.txt` file

## Installation
Clone the repository to your local machine using the following:

git clone https://github.com/yourusername/amazon-scraper.git

## Utilization
To run the code:

1. Run the scraper in your terminal: python3 `amazon_scraper.py`
2. When prompted, paste an Amazon.ca search URL into the terminal.

The code will scrape the data from each product on the page, return a preview of the `DataFrame`, and save the results into a file called `amazon_data.csv` on your local machine.

# Disclaimer
Use responsibly and respect Amazon’s robots.txt and scraping policies.
https://www.amazon.ca/robots.txt
