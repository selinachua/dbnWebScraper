'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains the constants used throughout the scraper.
'''

import sys

# Windows Slash is '\\' whereas Unix is '/'
# SLASH = '\\'
SLASH = '/'

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
TEMP_CSV = sys.path[0] + "/temp/output.csv"
# TEMP_PDF = sys.path[0] + SLASH + "temp" + SLASH + "temp.pdf"
# EXCEL_SHEET = sys.path[0] + SLASH + "results" + SLASH
TEMP_CSV = sys.path[0] + SLASH + "temp" + SLASH + "output.csv"

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

# PDF Page 1 Hospital Cover Info Columns
SERVICE = 0
INFO = 1

# PDF Page 2 Treatment Cover Column Names
SERVICE = 0
COVER = 1
WAITING_PERIOD = 2
BENEFIT_LIMITS = 3
MAX_BENEFITS = 4

# NEW PDF Page 2 Treatment Cover Column Names
SERVICE = 0
NEW_WAIT_PERIOD = 1
NEW_BENEFIT_LIMITS = 2
NEW_MAX_BENEFITS = 3

# ---- EXCEL SPREADSHEET CONSTANTS ---- 
COL_PDF_TYPE          = 1
COL_POL_NAME          = 2
COL_FUND_NAME         = 3
COL_PDF_LINK          = 4

# Criteria
COL_STATUS            = 5
COL_EXCESS            = 6
COL_MOPREM            = 7
COL_STATE             = 8
COL_ADULTS            = 9
COL_DPNDNTS           = 10
COL_AVAIL             = 11

# Hospital Cover
COL_POL_TYPE          = 12
COL_CORP              = 13
COL_HOSP_COVERED      = 14
COL_HOSP_NOT_COVERED  = 15
COL_HOSP_LIMITED      = 16
COL_WAIT_PERIODS      = 17
COL_COPAYMENT         = 18
COL_OTHER_HOSP        = 19

# General Services 
COL_GENERAL_DENTAL    = 20
COL_MAJOR_DENTAL      = 23
COL_ENDODONTIC        = 26
COL_ORTHODONTIC       = 29
COL_OPTICAL           = 32
COL_NONPSBPHARM       = 35
COL_PHYSIO            = 38
COL_CHIRO             = 41
COL_PODIATRY          = 44
COL_PSYCH             = 47
COL_ACUPUNC           = 50
COL_NATUR             = 53
COL_MASSAGE           = 56
COL_HEARING           = 59
COL_BLOOD             = 62
COL_AUDIO             = 65
COL_NATAL             = 68
COL_CHINESE           = 71
COL_DIETARY           = 74
COL_EXERCISE_PHYSIO   = 77
COL_EYE_THERAPY       = 80
COL_HEALTH_LIFE       = 83
COL_HOME_NURSING      = 86
COL_OCCUPATIONAL_THER = 89
COL_ORTHOTICS         = 92
COL_OSTEOPATHY        = 95
COL_SPEECH            = 98
COL_VACCINATIONS      = 101


# Other
COL_AMBULANCE_EMER    = 104
COL_AMBULANCE_WP      = 104
COL_AMBULANCE_FEE     = 105
COL_AMBULANCE_LIMITS  = 105
COL_AMBULANCE_OTHER   = 106
COL_AMBULANCE_MAX_BEN = 106
COL_OTHER             = 107
COL_MEDICARE          = 108
COL_ISSUE_DATE        = 109
COL_AVAIL_FOR         = 110
COL_PROV_ARR          = 111
COL_AGE_DISC          = 112
COL_TRAV_ACCOM_BEN    = 113
COL_POL_ID            = 114
COL_ACCIDENT_COV      = 115


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

