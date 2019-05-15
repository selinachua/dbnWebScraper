'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains the code for web scraping.
# It scrapes the given link for PDFs and information 
# on its hospital services.
'''

import requests
from requests.exceptions import RequestException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import *
from time import sleep
from policy import WebPolicy

def scrape_single_criteria(criteria, fund_links):
    '''
    Scrapes all fund_links for passed in criteria.

    Since each fund can have more than one pdf link if it 
    has more than one excess value, so we make a 2D 
    dictionary in this form:

    e.g.:
    fund_pdfs = {
        ACA: {pdf_link: Policy class with information}
        ...
    }
    '''
    browser = webdriver.Chrome()
    fund_pdfs = {}

    for fund in fund_links:
        print(f"... Scraping {fund} ...")
        browser.get(get_link(fund, fund_links))
        nav_to_policy_page(browser)
        click_criteria(browser, criteria)
        scrape_results(browser, fund_pdfs, fund, criteria)

    return fund_pdfs


def scrape_results(browser, fund_pdfs, fund, criteria):
    '''
    This function goes through all the results of a given
    criteria and scrapes for their PDF web links. This is 
    stored in a dictionary, where the key is the fund and
    the value is a Policy class.
    '''
    fund_pdfs[fund] = {}

    results_exist = browser.find_element_by_xpath("//div[@id='Results']/p").text
    # No policies found
    if NO_POLICIES_STR in results_exist:
        print(f"No policies found for {fund}.\n")
        return

    # Clicks all checkboxes and adds to compare page.
    checkboxes = browser.find_elements_by_xpath(f"//input[@name='SelectedProductKeys']")
    n_pols = len(checkboxes)
    for box in checkboxes:
        statuses = browser.find_elements_by_xpath("//td[@class='ResultColumn_Status']//span")
        for n in range(n_pols):
            statuses[n] = statuses[n].text
        box.click()
    compare_btn = browser.find_element_by_id("ResultsSubmitCompare")
    compare_btn.click()

    # Grabs current card in focus.
    # Waits until the cards have loaded.
    focus = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@class='product focus']"))
    )
    # We expand hospital section to grab all the covered hospital services.
    try:
        hosp_section = focus.find_element_by_class_name("hospitalsection")
        expand_btn = hosp_section.find_element_by_class_name("expand")
        expand_btn.click()
    except:
        pass

    # For all the policies found.
    for n in range(n_pols):
        print(f"... Scraping {n+1} of {n_pols} ...", end='\r')
        focus = browser.find_element_by_xpath("//*[@class='product focus']")
        # Gets status of the policy.
        status = statuses[n]
        # Finds all excess if there are multiple.
        if criteria.pol_type == HOSPITAL or criteria.pol_type == COMBINED_TREATMENT:
            all_excess = focus.find_elements_by_tag_name('li')
            for excess in all_excess:
                try:
                    excess.click()
                except: 
                    continue
                pdf_link = focus.find_element_by_xpath("//h2/a").get_attribute('href')
                pol = create_policy(browser, focus, status, criteria, pdf_link)
                fund_pdfs[fund][pdf_link] = pol
        else:
            pdf_link = focus.find_element_by_xpath("//h2/a").get_attribute('href')
            pol = create_policy(browser, focus, status, criteria, pdf_link)
            fund_pdfs[fund][pdf_link] = pol

        # Closes the current focus card, making a new card the focus card.
        close_btn = focus.find_element_by_xpath("//h1/button[@title='Click to close']")
        close_btn.click()
    print('\n')

    return fund_pdfs
        
        
def print_pdf_links(fund_pdfs, fund):
    for link in fund_pdfs[fund]:
        print(f"--- LINK: {link}")
        policy = fund_pdfs[fund][link]
        print(policy)


def create_policy(browser, focus, status, criteria, pdf_link):
    '''
    Returns a Policy object given the current focus web element.
    Add as needed.
    '''
    fund_name = focus.find_element_by_xpath("//h1/a").text
    pol_name = focus.find_element_by_xpath("//h2/a").text
    premium = focus.find_element_by_class_name('premium').text
    try:
        co_pay = focus.find_element_by_xpath("//div[@class='copayment']//span").text 
        excess = focus.find_element_by_xpath("//div[@class='excess']//span[@class='selected']").text
        hosp_section = focus.find_element_by_class_name("hospitalsection")
        hosp_tier = hosp_section.find_element_by_tag_name('span').text
        hosp_accom = focus.find_element_by_xpath("//div[@class='cover']//span[@class='sr-only']").text
        # Grabs all the hospital covered and non covered things.
        covered = []
        not_covered = []
        limited_cover = []
        covers = hosp_section.find_elements_by_xpath("//div/div[@class='cover']")
        get_hosp_covers(covers, covered, not_covered, limited_cover)
        age_disc = focus.find_element_by_xpath("//div[@class='covered']//div").text
        medicare = focus.find_element_by_xpath("//div[@class='medicare']//span").text 
    except:
        covered = ['-']; not_covered = ['-']; limited_cover = ['-']
        hosp_tier = "None"
        co_pay = "None"
        excess = "None"
        hosp_accom = "None"
        age_disc = "None"
        medicare = "None"

    pol_id = pdf_link[len(MAIN_URL + DOWNLOAD_LINK):]
    

    new_pol = WebPolicy(fund_name, pol_name, pdf_link, status, criteria, premium, excess, co_pay, age_disc,
        medicare, hosp_accom, hosp_tier, covered, not_covered, limited_cover, pol_id)

    return new_pol


def get_hosp_covers(covers, covered, not_covered, limited_cover):
    '''
    Gets all the hospital covered and non covered things.
    '''
    for cover in covers:
        cover_name = cover.find_element_by_tag_name('a').text
        if cover_name == '':
            continue
        cover_class = cover.find_element_by_tag_name('div').get_attribute('class')
        if cover_class == "notCovered":
            not_covered.append(cover_name)
        elif cover_class == "Restricted":
            limited_cover.append(cover_name)
        elif cover_class == "covered":
            covered.append(cover_name)
        if 'Weight loss surgery' in cover_name:
            break


def click_criteria(browser, criteria):
    '''
    Clicks on the criteria on the policies page.
    '''
    btn_grps = browser.find_elements_by_class_name("btn-group")
    click_btn(btn_grps[STATE], criteria.state)
    click_btn(btn_grps[ADULTS], criteria.adults)
    click_btn(btn_grps[DPNDNTS], criteria.dpndnts)
    click_btn(btn_grps[TREATMENT], criteria.pol_type)
    click_btn(btn_grps[AVAIL], criteria.status)
    click_btn(btn_grps[CORP], criteria.corp)
    browser.find_element_by_id("InsurerQuestionsSubmit").submit()


def click_btn(elem, type):
    '''
    Clicks on the button in the criteria page.
    '''
    btn = elem.find_elements_by_css_selector(".btn-phsearch")
    btn[type].click()


def nav_to_policy_page(browser):
    '''
    Finds the policy button and navigates to it
    '''
    policy_btn = browser.find_element_by_id('nav_policies')
    policy_btn.click()


def get_link(fund, fund_links):
    '''
    Returns the actual fund_link given a fund. 
    '''
    return MAIN_URL + fund_links[fund][H_REF]


def create_all_criteria():
    '''
    Creates all the possible criterias for answering the Step 1 -
    Type of Cover form. 
    '''
    f = open(CRITERIA_FILE, "w+")
    # Cover all criterias in loop
    for state in range(MAX_STATE + 1):
        for adults in range(MAX_ADULTS + 1):
            for dpndnts in range(MAX_DPNDNTS + 1):
                for treatment in range(MAX_TREATMENT + 1):
                    for avail in range(MAX_AVAIL + 1):
                        for corp in range(MAX_CORP + 1):
                            criteria = str(state) + str(adults) + str(dpndnts) + str(treatment) + str(avail) + str(corp)
                            f.write(criteria + "\n")
    f.close()


def get_fund_links(soup):
    '''
    Goes through the Health Insurers table and creates a dictionary 
    called fundLinks, which is returned. Key of dictionary is the code, 
    and value is a tuple containing (title, href).
    e.g.
    fundLinks = {
        AHM: (ahm health insurance, /dynamic/Insurer/Details/AHM)
        AUF: (Australian Unity Health Limited, /dynamic/Insurer/Details/AUF)
        ...
    }
    '''
    # Create a dictionary for fundLinks.
    # Key: ATO ID - e.g. AHM, AUF, etc.
    # Value: href link to Details page.
    fund_links = {}

    # Creates a list of TAGS that correspond to the table's rows.
    fund_elems = soup.find_all('tr')
    # Removes header row from table.
    fund_elems = fund_elems[1:] 

    # For every row, we split each cell into elements of an array called cell.
    # Thus, for every row, we can access cell_array[0] for Insurer,
    # cell[1] for ATO ID, and etc.
    for elem in fund_elems:
        cell_array = elem.find_all('td')

        href_link = cell_array[0].find('a').get('href')
        elem_title = cell_array[0].find('a').get('title')
        elem_ID = cell_array[1].string

        fund_links[elem_ID] = (elem_title, href_link)

    return fund_links


def get_url(url):
    '''
    Downloads the webpage from the url given.
    '''
    # Try to get the html. Closes the link if it does not work.
    try:
        resp = requests.get(url)
        if is_good_response(resp):
            return resp.content
        else:
            return None
    # If we fail to call requests.get
    except RequestException as e:
        # # # DO THIS # # # 
        print(str(e))


def is_good_response(resp):
    '''
    Returns True if the response seems to be HTML, False otherwise.
    '''
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200 
            and content_type is not None 
            and content_type.find('html') > -1)


def closePopup(browser):
    '''
    Closes browser. 
    '''
    try:
        popup = browser.find_element_by_xpath("//*[@class='close']")
        popup.click()
    except:
        pass