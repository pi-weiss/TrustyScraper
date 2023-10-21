# Trustpilot Scraper

***

This script provides a web scraper that extracts reviews from Trustpilot.com. It uses the BeautifulSoup library to parse the HTML of the website and extract the relevant information. The extracted data is then saved to a CSV file.
## Dependencies

***

- pandas
- BeautifulSoup

## Usage

***

Call `scrape_reviews("company_name", first_page)`
- The first page is 1 by default
- The script will automatically search for the last page

_Note that there may be changes to the DOM and the class names may need to be updated_