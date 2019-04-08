'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains the constants used throughout the scraper.
'''

import sys

# Windows Slash is '\\' whereas Unix is '/'
SLASH = '\\'

# ==================================================================
# Following constants are links required for scraping.
# ==================================================================

MAIN_URL       = "https://www.privatehealth.gov.au"
FUND_LIST_LINK = MAIN_URL + "/dynamic/Insurer"
RESULTS_LINK = "/ResultsPartial/"
COMPARE_LINK = FUND_LIST_LINK + "/Compare/"
GET_COMPARE_LINK = MAIN_URL + "/dynamic/Search/Compare/"
DOWNLOAD_LINK = "/dynamic/Download/"
EXCEL_SHEET = sys.path[0] + "/results/"
TEMP_PDF = sys.path[0] + "/temp/"
# TEMP_PDF = sys.path[0] + SLASH + "temp" + SLASH + "temp.pdf"
# EXCEL_SHEET = sys.path[0] + SLASH + "results" + SLASH

RESUME_FILE   = 'resume.txt'
CRITERIA_FILE = 'criteria.txt'
SCRAPED_FILE  = 'scraped.txt'

# ==================================================================
# Following constants are for Criteria Selection in web scraping.
# ==================================================================

# Criteria Selection
STATE     = 0
ADULTS    = 1
DPNDNTS   = 2
TREATMENT = 3
AVAIL     = 4
CORP      = 5

# Where will you be living?
ACT = 0
NSW = 1
NT  = 2
QLD = 3
SA  = 4
TAS = 5
VIC = 6
WA  = 7
MAX_STATE = 7
states = ["ACT", "NSW", "NT", "QLD", "SA", "TAS", "VIC", "WA"]

# How many adults will be covered by this policy
SINGLE     = 0
DOUBLE     = 1
NO_ADULTS  = 2
MAX_ADULTS = 2
n_adults = ["One", "Two", "NoAdults"]

# Who are the oldest dependants to be covered by this policy?
NO_DEPENDANTS = 0
CHILD         = 1
YOUNG_ADULTS  = 2
MAX_DPNDNTS   = 2
dpndnts = ["None", "Children", "YoungAdults"]

# What type of policy do you need?
HOSPITAL           = 0 
GEN_TREATMENT      = 1
COMBINED_TREATMENT = 2
AMBULANCE_ONLY     = 3
MAX_TREATMENT      = 3
policy = ["Hospital", "General", "Combined", "Ambulance"]

# Show products
OPEN      = 0
CLOSED    = 1
BOTH      = 2
MAX_AVAIL = 2
avail = ["Open", "Closed", "Both"]

# Include Corporate Products in the search results
NO_CORPORATE   = 0
INCL_CORPORATE = 1
MAX_CORP       = 1
corp = ["NoCorporate", "IncludeCorporate"]

# ==================================================================
# Constants used for PDF scraping.
# ==================================================================

OLD_PDF = 0
NEW_PDF = 1

OLD_TITLE = "Private Health Insurance Standard Information Statement"
NEW_TITLE = "Private Health Information Statement"


# ==================================================================
# Miscellaneous constants.
# ==================================================================

TITLE = '''============== dbn Web Scraper ==============='''
LAST_UPDATE = "... Last updated 02/04/19 ..."
NO_POLICIES_STR = "There are no policies that match your selections."

# H_REF of a fund link is stored as a tuple in the dictionary value.
H_REF = 1 

# Online sources
PDF_TO_TEXT_SRC = "https://stackoverflow.com/questions/52416268/how-to-use-pdfminer-sixs-pdf2txt-py-in-python-script-and-outside-command-line"

