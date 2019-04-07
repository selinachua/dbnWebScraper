'''
This file is only designed for random testing.
'''

import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from constants import *
from time import sleep
from policy import Policy
from web_scraper import *
from criteria import Criteria

browser = webdriver.Chrome()

browser.get("https://www.privatehealth.gov.au/dynamic/Insurer/Details/FAI")
nav_to_policy_page(browser)

criteria = Criteria("000000")
click_criteria(browser, criteria)


results_exist = browser.find_element_by_xpath("//div[@id='Results']/p").text
if NO_POLICIES_STR in results_exist:
    print("NO POLICIES FOUND.")
    exit(1)
fund_pdfs[fund] = {}

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

# Waits until the cards have loaded.
for n in range(n_pols):
    # Grabs current card in focus.
    focus = WebDriverWait(browser, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[@class='product focus']"))
    )
    # Gets status of the policy.
    status = statuses[n]
    # Finds all excess if there are multiple.
    all_excess = focus.find_elements_by_tag_name('li')
    for excess in all_excess:
        print(excess.text)
        excess.click()
        pol = create_policy(focus, status, criteria)
        pdf_link = focus.find_element_by_xpath("//h2/a").get_attribute('href')
        fund_pdfs[fund][pdf_link] = pol
    # Closes the current focus card, making a new card the focus card.
    close_btn = focus.find_element_by_xpath("//h1/button[@title='Click to close']")
    close_btn.click()

# print_pdf_links(fund_pdfs, fund)



# checkboxes = browser.find_elements_by_xpath(f"//input[@name='SelectedProductKeys']")
# n_pols = len(checkboxes)
# for box in checkboxes:
# box.click()
# break
# compare_btn = browser.find_element_by_id("ResultsSubmitCompare")
# compare_btn.click()

# focus = WebDriverWait(browser, 10).until(
#     EC.presence_of_element_located((By.XPATH, "//*[@class='product focus']"))
# )
# all_excess = focus.find_element_by_class_name('excess').find_elements_by_tag_name('li')
# for excess in all_excess:
#     print(excess.text)





# print(focus.text)
# for excess in all_excess:
#     excess.click()
#     print(excess.text)
#     # print(excess.find_element_by_xpath("/following-sibling::p"))