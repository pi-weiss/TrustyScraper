# Scrape reviews from Trustpilot.com and save to csv file using BeautifulSoup

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import re
from datetime import datetime

# Function to get page and return BeautifulSoup object
def get_page(company_name, page_num):
    
    # Get the page
    if page_num == 1:
        review_page = requests.get(f"https://www.trustpilot.com/review/{company_name}?languages=all")
    else:
        review_page = requests.get("https://www.trustpilot.com/review/{}?languages=all&page={}".format(company_name,page_num))

    # Create BeautifulSoup object
    soup = BeautifulSoup(review_page.text, "html.parser")

    return soup



# Function to scrape reviews from Trustpilot.com and save to csv file
# Takes the subdirectory/company name as an argument
def scrape_reviews(company, first_page=1):

    # Initialize lists to store scraped data
    review_titles = []
    review_texts = []
    review_dates = []
    review_stars = []
    review_languages = []

    # CSS selectors on Trustpilot.com
    section_class = "styles_reviewContentwrapper__zH_9M"
    text_class = "styles_reviewContent__0Q2Tg"
    title_class = "styles_reviewHeader__iU9Px"
    pagination_class = "styles_pagination__6VmQv"

    # Get the first page
    page = get_page(company, first_page)

    # Get last page number
    last_page = int(page.find("div", {"class":pagination_class}).find_all("a")[-2].string)

    # Loop through each page
    for current_page in range(first_page, last_page + 1):

        # Find all reviews on the page
        reviews = page.find_all("section", {"class":section_class})
        time.sleep(random.randint(0, 3))

        # Loop through each review on the page
        for review in reviews:

            # Find the review title and append to list
            review_title = review.find("h2").string
            review_titles.append(review_title)

            # Find the review text and append to list; if no text, append review title
            if re.search("Date of.", review.find("p").get_text()) != None:
                review_text = review.find("h2").string
            else:
                review_text = review.find("p").get_text()
            review_texts.append(review_text)

            # Find the review date and append to list
            review_date = review.find("time")["datetime"]
            review_dates.append(review_date)

            # Find the review star rating and append to list
            review_star = review.find("div",{"class":title_class})["data-service-review-rating"]
            review_stars.append(review_star)

            # Find the review language and append to list; if no language, append "nd"
            try:
                review_language = review.find("div",{"class":text_class})["lang"]
            except KeyError:
                review_language = "nd"
            
            review_languages.append(review_language)
        
        # Get the next page
        page = get_page(company, current_page+1)

    # Create a dataframe from the lists
    df = pd.DataFrame({
        'Title': review_titles,
        'Text': review_texts,
        'Date': review_dates,
        'Stars': review_stars,
        'Language': review_languages
    })

    # Change the date format
    for i in df.index:
        date = df.at[i,"Date"]
        df.at[i,"Date"] = date.replace(date[10:],"")

    # save the dataframe to a csv file
    today = datetime.today()
    trustpilot_reviews = df.to_csv("tests/" + f"{today:%Y%m%d}_{company}_trustpilot_reviews_raw.csv")
    


scrape_reviews("villycustoms.com")

