from bs4 import BeautifulSoup
import requests
import pandas as pd


def get_title(soup):
    try:
        # Outer Tag Object
        title_string = soup.find("span", attrs={"id": 'productTitle'}).string.strip()

    except AttributeError:
        title_string = ""

    return title_string


def get_price(soup):
    try:

        price_string = soup.find("span", attrs={"class": "a-offscreen"}).string.strip()

    except AttributeError:
        price_string = ""

    return price_string


def get_rating(soup):
    try:
        rating = soup.find("i", attrs={'class': 'a-icon a-icon-star a-star-4-5'}).string.strip()

    except AttributeError:
        try:
            rating = soup.find("span", attrs={'class': 'a-icon-alt'}).string.strip()
        except:
            rating = ""

    return rating


def get_reviews(soup):
    try:
        review_count = soup.find("span", attrs={'id': 'acrCustomerReviewText'}).string.strip()

    except AttributeError:
        review_count = ""

    return review_count


def get_availability(soup):
    try:
        available = soup.find("div", attrs={'id': 'availability'})
        available = available.find("span").string.strip()

    except AttributeError:
        available = "Not Available"

    return available
