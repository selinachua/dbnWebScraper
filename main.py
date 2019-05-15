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
from pdf_scraper import *
from bs4 import BeautifulSoup
from criteria import Criteria
import datetime
import shutil

def save_state(crit_file, resume_file, seen_file):
    '''
    Saves the current state on an exception. 
    '''
    print("... Saving state ...")
    seen_text = seen_file.read()
    # Writes criteria that haven't been scraped into resume.txt.
    for line in crit_file:
        new_line = line[:len(line)-1]
        if new_line not in seen_text:
            resume_file.write(line)


def main():
    print(TITLE)

    resume = int(input("Type 1 if you are resuming webscraper \
and 0 if you are starting a new webscrape:\n"))
    
    print("... Starting webscrape ...\n")
        
    # Downloads the URL of the fund list link.
    try:
        fund_list_url = get_url(FUND_LIST_LINK)
        fund_list_soup = BeautifulSoup(fund_list_url, 'html.parser')
        fund_links = get_fund_links(fund_list_soup)
    except:
        print("ERROR: Fund list page broken. Aborted.")
        exit(1)
    print(f"... Found {len(fund_links)} health fund links ...\n")

    # Copies resume.txt over into criteria.txt
    if resume:
        try:
            shutil.copyfile(RESUME_FILE, CRITERIA_FILE)
        except:
            print("ERROR: Resume file does not exist. Aborting.")
            exit(1)
        scraped_file = open(SCRAPED_FILE, 'a+')
    # Creates all possible criterias and puts it in CRITERIA_FILE.
    else:
        create_all_criteria()
        print("... Created criteria file ...")
        scraped_file = open(SCRAPED_FILE, 'w+')
    
    crit_file = open(CRITERIA_FILE, 'r')

    for line in crit_file:
        # 1. Grabs the criteria.
        orig_line = line
        line = line[:len(line)-1]
        print(f"... Scraping online for {line} criteria ...")
        cur_criteria = Criteria(list(line))
        try:
            # 2. Gets all pdf_links for cur_criteria in a 2D dictionary.
            pdfs_dict = scrape_single_criteria(cur_criteria, fund_links)
            print(f"... Scrape online for {line} SUCCESSFUL ...\n")
            # 3. Creates excel sheet.
            sheet = EXCEL_SHEET + "Criteria " + line + " " + \
                datetime.datetime.now().strftime("%d %B %Y at %H.%M") + ".xlsx"
            create_excel(sheet)
            # 4. Scrapes pdfs into sheet.
            print(f"... Scraping pdfs into excel ...")
            scrape_all_pdfs(pdfs_dict, sheet, cur_criteria.pol_type)
            # 5. Update contents of scraped_file.
            scraped_file.write(orig_line)
            print(f"... Completed scraping for criteria {line} ...")
        except Exception as e:
            print("!!! ERROR !!!")
            scraped_file.close()
            crit_file.close()
            scraped_file = open(SCRAPED_FILE, 'r')
            resume_file = open(RESUME_FILE, 'w+')
            crit_file = open(CRITERIA_FILE, 'r')
            save_state(crit_file, resume_file, scraped_file)
            crit_file.close()
            scraped_file.close()
            resume_file.close()
            print(f"... Aborting, state saved ... ERROR: {str(e)} ...")
            exit(1)
    # Clean up!
    crit_file.close()
    scraped_file.close()

if __name__ == "__main__":
    main()