from bs4 import BeautifulSoup
import requests
from requests.exceptions import RequestException
from scraping_data_classes import get_title, get_price, get_rating, get_reviews, get_availability
import pandas as pd
import numpy as np
import urllib.robotparser
import time
import random

#Header is needed to scrape, maybe use selenium or a selection of different headers as to not use my own LOL.
HEADERS = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
           'Accept-Language' : 'en-US, en;q=0.5'}

#Scraping function, its only parameter is the url given by the user.
def scraper(url):
    rp = urllib.robotparser.RobotFileParser() #To ensure adherence to Amazons scraping guidelines, we create a parser.
    rp.set_url("https://www.amazon.ca/robots.txt") #Giving the parser Amazons rules surrounding scraping.
    rp.read()  # FINISH SETTING UP THE ROBOT PARSER FUCKKKKKK DONT FORGET

    #Checking if the robot is allowed to scrape the desired data.
    if rp.can_fetch(HEADERS["User-Agent"], url):
        webpage = requests.get(url, headers=HEADERS) #If allowed it begins scraping
        contentSoup = BeautifulSoup(webpage.content, "html.parser") #BeautifulSoup fetches all content from the webpage
    else:
        print(f'Access denied to : {url}') #If scraping the desired data is against the regulations, it notifies the user
        exit() #Exit the code

    #The links variable is all products on the page, which we later scrape for the desired data
    links = contentSoup.find_all("a", attrs={'class': "a-link-normal s-no-outline"})
    productLinks = [] #The link for each product of the given search page

    #THe following loop ensures all links are uniform, otherwise some links may have slight differences which can lead to errors
    for link in links:
        href = link.get('href')
        if href.startswith("/"):  # It's a relative URL
            productLinks.append("https://www.amazon.ca" + href) #COME BACK TO THIS, MAY BE ABLE TO OPTIMIZE
        elif href.startswith("http"):
            productLinks.append(href)
        else:
            # Handle unexpected URL formats
            productLinks.append("https://www.amazon.ca" + href)

    #Creating the dictionary for the data MAYBE REMOVE THIS AND DIRECTLY MAKE DATAFRAME
    productData = {"Title": [], "Price": [], "Rating": [], "Reviews": [], "Availability": []}

    #Sorting data into their respective columns in the dictionary
    for link in productLinks:
        if rp.can_fetch(HEADERS["User-Agent"], link): #Checks if the scraper can fetch the data from the specific project
            try:
                productWebpage = requests.get(link, headers=HEADERS) #WRITE A COMMENT
                productWebpage.raise_for_status()
                newContentSoup = BeautifulSoup(productWebpage.content, "html.parser") #Retrieves the  data from the specific product

                productData["Title"].append(get_title(newContentSoup)) #Title
                productData["Price"].append(get_price(newContentSoup)) #Price
                productData["Rating"].append(get_rating(newContentSoup)) #Rating (1-5 stars)
                productData["Reviews"].append(get_reviews(newContentSoup)) #Number of Reviews
                productData["Availability"].append(get_availability(newContentSoup)) #Availability (True or not True)
            except RequestException as e:
                print(f'Access denied to : {link} error: {e}')
                continue

            #Waiting 1.5 seconds between each loop to ensure amazon does not detect the bot
            time.sleep(random.uniform(1.5, 3.5))


    #Turning the dictionary into a dataframe
    amazon_df = pd.DataFrame.from_dict(productData)

    #Transforming each column to the intended type
    amazon_df = amazon_df.astype({
        "Title": "string",
        "Rating": "string",
        "Reviews": "string",
        "Availability": "string"
    })

    #Replacing any titles not found with NA values
    amazon_df["Title"] = amazon_df["Title"].replace("", np.nan).fillna('N/A')

    #Transforming the price column to drop any unneeded symbols and prepare for any numeric manipulation
    amazon_df['Price'] = amazon_df['Price'].astype(str).str.replace(r'[^\d.]', '', regex=True)
    amazon_df['Price'] = pd.to_numeric(amazon_df['Price'], errors='coerce')

    return amazon_df


    #Below is what I am currently working on
    #Drop rows with invalid price
    #amazon_df.dropna(subset=['Price'], inplace=True)

    #Finding basic statistical values for the price, MAY NOT BE NEEDED BUT MAYBE ALSO ADD A VALUE DETERMINED BY RATING RELATIVE TO NUMBER OF REVIEWS
    #amazon_stats = pd.DataFrame({
    #    "Mean Price": [amazon_df["Price"].mean()],
    #    "Median": [amazon_df["Price"].median()],
    #    "Mode": [amazon_df["Price"].mode().iloc[0] if not amazon_df["Price"].mode().empty else np.nan]
    #})

    #returning the product data and price statistics
    #return amazon_df, amazon_stats

#amazon_df.to_csv("amazon_data.csv", header=True, index=False)
