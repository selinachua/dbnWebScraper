'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains the main code of the scraper.
# What it does:
#    1. Scrapes a given link for PDFs and downloads them.
#    2. Scraped the PDF for information and places info into a
#       spreadsheet.
'''

from constants import *
from web_scraper import *
from bs4 import BeautifulSoup
from criteria import Criteria

def main():
    print(TITLE)
    print("... Starting a new webscrape ...\n")
        
    # Downloads the URL of the fund list link.
    fund_list_url = get_url(FUND_LIST_LINK)
    fund_list_soup = BeautifulSoup(fund_list_url, 'html.parser')
    fund_links = get_fund_links(fund_list_soup)
    print(f"... Found {len(fund_links)} health fund links ...\n")

    # Creates all possible criterias and puts it in CRITERIA_FILE.
    create_all_criteria()
    print("... Created criteria file ...")
    crit_file = open(CRITERIA_FILE, 'r')

    for line in crit_file:
        # 1. Grabs the criteria.
        line = line[:len(line)-1]
        print(f"... Scraping online for {line} criteria ...")
        cur_criteria = Criteria(list(line))
        # 2. Gets all pdf_links for cur_criteria in a 2D dictionary.
        pdfs = scrape_single_criteria(cur_criteria, fund_links)

    crit_file.close()

if __name__ == "__main__":
    main()