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

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import BytesIO
from pathlib import Path
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font
import requests, datetime, re, tabula, sys, csv

from constants import *
from service import Service
from oldpdf_classes import oldPdfInfo
from policy import WebPolicy
from criteria import Criteria


def scrape_all_pdfs(pdf_dict, sheet):
    '''
    This function is the main pdf_scraper function. It iterates 
    through all the pdfs inside the dictionary and scrapes all
    information into the passed in excel sheet.
    '''
    wb = load_workbook(sheet)
    ws = wb.active
    input_row = 2
    for fund in pdf_dict:
        pdf_num = 1
        for link in pdf_dict[fund]:
            pdf_dest = TEMP_PDF + fund + str(pdf_num) + ".pdf"
            download_pdf(link, pdf_dest)
            pdf_info = scrape_pdf(pdf_dest)
            # Popualate the excel spreadsheet.
            if pdf_info.pdf_type == OLD_PDF:
                old_populate_excel(pdf_dict[fund][link], pdf_info, ws, input_row)
            elif pdf_info.pdf_type == NEW_PDF:
                new_populate_excel()
            input_row += 1
            pdf_num += 1
            break
        break
    wb.save(sheet)

    # Clean up temp folder using shutil.rmtree()


def scrape_pdf(pdf_dest):
    '''
    This function scrapes the pdf according to its type.
    '''
    pdf_text = pdf_to_text(pdf_dest)
    pdf_type = get_pdf_type(pdf_text)
    
    if pdf_type == NEW_PDF:
        pdf_info = scrape_new_pdf(pdf_text)
    elif pdf_type == OLD_PDF:
        pdf_info = scrape_old_pdf(pdf_text)
    else:
        pdf_info = "Couldn't identify PDF type."

    return pdf_info


def scrape_new_pdf(pdf_text):
    print("Scraping new pdf...")
    # tables = tabula.read_pdf(f"{sys.path[0]}/temp/NKHZ20.pdf", pages=, flavor='lattice')
    # print(tables)
    # tabula.convert_into(f"{sys.path[0]}/temp/NKHZ20.pdf", TEMP_CSV, multiple_tables=True, spreadsheet=True, pages=[1,2], output_format='csv', encoding='utf-8')
    # exit(1)


def old_populate_excel(web_policy, pdf_info, ws, input_row):
    # Input web policy information.
    if pdf_info.pdf_type == OLD_PDF:
        ws.cell(row=input_row, column=COL_PDF_TYPE).value = "OLD"
    elif pdf_info.pdf_type == NEW_PDF:
        ws.cell(row=input_row, column=COL_PDF_TYPE).value = "NEW"

    ws.cell(row=input_row, column=COL_POL_NAME).value = web_policy.name
    ws.cell(row=input_row, column=COL_FUND_NAME).value = web_policy.fund_name
    ws.cell(row=input_row, column=COL_PDF_LINK).value = web_policy.pdf_link
    ws.cell(row=input_row, column=COL_STATUS).value = web_policy.status
    ws.cell(row=input_row, column=COL_MOPREM).value = web_policy.premium 
    ws.cell(row=input_row, column=COL_EXCESS).value = web_policy.excess
    ws.cell(row=input_row, column=COL_COPAYMENT).value = web_policy.co_pay
    ws.cell(row=input_row, column=COL_AGE_DISC).value = web_policy.age_disc
    ws.cell(row=input_row, column=COL_MEDICARE).value = web_policy.medicare
    ws.cell(row=input_row, column=COL_POL_ID).value = web_policy.id
    ws.cell(row=input_row, column=COL_STATE).value = states[web_policy.criteria.state]
    ws.cell(row=input_row, column=COL_ADULTS).value = states[web_policy.criteria.adults]
    ws.cell(row=input_row, column=COL_DPNDNTS).value = states[web_policy.criteria.dpndnts]
    ws.cell(row=input_row, column=COL_POL_TYPE).value = states[web_policy.criteria.pol_type]
    ws.cell(row=input_row, column=COL_CORP).value = states[web_policy.criteria.corp]
    ws.cell(row=input_row, column=COL_PROV_ARR).value = pdf_info.prov_arr
    ws.cell(row=input_row, column=COL_ISSUE_DATE).value = pdf_info.issue_date
    ws.cell(row=input_row, column=COL_AVAIL_FOR).value = pdf_info.avail_for
    ws.cell(row=input_row, column=COL_WAIT_PERIODS).value = pdf_info.wait
    ws.cell(row=input_row, column=COL_OTHER).value = pdf_info.general_other
    ws.cell(row=input_row, column=COL_TRAV_ACCOM_BEN).value = web_policy.hosp_accom

     # Inputting hospital cover details.
    covered = ""
    for c in web_policy.covered:
        covered += f"{c}, "
    ws.cell(row=input_row, column=COL_HOSP_COVERED).value = covered
    not_covered = ""
    for c in web_policy.not_covered:
        not_covered += f"{c}, "
    ws.cell(row=input_row, column=COL_HOSP_NOT_COVERED).value = not_covered
    limited_cover = ""
    for c in web_policy.limited_cover:
        limited_cover += f"{c}, "
    ws.cell(row=input_row, column=COL_HOSP_LIMITED).value = limited_cover
    ws.cell(row=input_row, column=COL_OTHER_HOSP).value = web_policy.other_hosp_feature

    # Inputting general details.
    for service in pdf_info.services:
        col = ''
        s = service.lower()
        print(s)
        if 'general' in s:
            col = COL_GENERAL_DENTAL
        elif 'major' in s:
            col = COL_MAJOR_DENTAL
        elif 'endodontic' in s:
            col = COL_ENDODONTIC
        elif 'orthodontic' in s:
            col = COL_ORTHODONTIC
        elif 'optical' in s:
            col = COL_OPTICAL
        elif 'non pbs' in s:
            col = COL_NONPSBPHARM
        elif 'exercise physiology' in s:
            col = COL_EXERCISE_PHYSIO
        elif 'physio' in s:
            col = COL_PHYSIO
        elif 'chiro' in s:
            col = COL_CHIRO
        elif 'podiatry' in s:
            col = COL_PODIATRY
        elif 'psychology' in s:
            col = COL_PSYCH
        elif 'acupuncture' in s:
            col = COL_ACUPUNC
        elif 'naturopathy' in s:
            col = COL_NATUR
        elif 'massage' in s:
            col = COL_MASSAGE
        elif 'hearing aids' in s:
            col = COL_HEARING
        elif 'glucose' in s:
            col = COL_BLOOD
        elif 'audiology' in s:
            col = COL_AUDIO
        elif 'antenatal' in s:
            col = COL_NATAL
        elif 'chinese' in s:
            col = COL_CHINESE
        elif 'dietetics' in s:
            col = COL_DIETARY
        elif 'orthoptics' in s:
            col = COL_EYE_THERAPY
        elif 'health management' in s:
            col = COL_HEALTH_LIFE
        elif 'nursing' in s:
            col = COL_HOME_NURSING
        elif 'occupational therapy' in s:
            col = COL_OCCUPATIONAL_THER
        elif 'orthotics' in s:
            col = COL_ORTHOTICS
        elif 'osteopathy' in s:
            col = COL_OSTEOPATHY
        elif 'speech' in s:
            col = COL_SPEECH
        elif 'vaccinations' in s:
            col = COL_VACCINATIONS
        elif 'ambulance' in s and pdf_info.pdf_type == OLD_PDF:
            col = COL_AMBULANCE_WP
        
        if col != '':
            ws.cell(row=input_row, column=col).value = pdf_info.services[service].wait 
            ws.cell(row=input_row, column=col+1).value = pdf_info.services[service].limits 
            ws.cell(row=input_row, column=col+2).value = pdf_info.services[service].max_benefits


def scrape_old_pdf(pdf_text):
    '''
    This function scrapes the old pdf for wanted information.
    '''
    print("Scraping old pdf...")

    pdf_hosp_info = read_hosp_page_old_pdf(pdf_text)
    pdf_info = read_general_old_pdf(pdf_text, pdf_hosp_info)
    return pdf_info
    


def read_general_old_pdf(pdf_text, oldpdf_class):
    '''
    This functions reads the general treatment page in the old pdf.
    '''
    # Converts the general table in PDF into CSV format. 
    tabula.convert_into(f"{sys.path[0]}/temp/NJKD20.pdf", TEMP_CSV, \
        lattice=True, spreadsheet=True, pages=2, output_format='csv')

    f = open(TEMP_CSV)
    csv_f = csv.reader(f)

    prov_arr = "None"
    services = {}
    for row in csv_f:
        # Special cases:
        if 'PROVIDER ARRANGEMENTS:' in row[SERVICE]:
            prov_arr = row[SERVICE]
        elif 'FEATURES' in row[SERVICE]:
            other = row[SERVICE]
        elif 'SERVICES' in row[SERVICE] \
            or not row[SERVICE]:
            continue
        # Get the general treatment stuff. 
        else:
            name = row[SERVICE]
            wait = row[WAITING_PERIOD]
            # If there is no waiting period, service is not covered.
            if '-' in wait:
                cover = "No"
            else:
                cover = "Yes"
            limit = row[BENEFIT_LIMITS]
            max_benefits = row[MAX_BENEFITS]
            # If max benefits is empty, then it is in limits and limit is the same as previous.
            if not max_benefits:
                max_benefits = limit 
                limit = '-'
            if cover == "Yes" and limit == '-':
                limit = "Same as previous."
            cur_service = Service(name, cover, wait, limit, max_benefits)
            print("CUR SERVICE", cur_service)
            services[name] = cur_service
    f.close()
    oldpdf_class.prov_arr = prov_arr
    oldpdf_class.services = services
    oldpdf_class.general_other = other
    return oldpdf_class



def read_hosp_page_old_pdf(pdf_text):
    '''
    This function reads the hospital page in the pdf and scrapes 
    for its issue date and available for.
    '''
    # Grabs issue date.
    try:
        issue_date = str(re.search(r'issued (.*)\n', pdf_text)).group(1)
    except:
        issue_date = "Can't find issue date"
    # Grabs available for information.
    first_lines = pdf_text.rsplit('\n')
    avail_for = ""
    for line in first_lines:
        if 'Residents' in line:
            avail_for = line
            break
    
    # Read rest of hospital page.
    tabula.convert_into(f"{sys.path[0]}/temp/NJKD20.pdf", TEMP_CSV, \
        lattice=True, spreadsheet=True, pages=1, output_format='csv')

    f = open(TEMP_CSV)
    csv_f = csv.reader(f)

    waiting_period = ""; payable = ""
    for row in csv_f:
        # Find waiting period.
        if 'HOW LONG ARE THE WAITING' in row[SERVICE]:
            waiting_period = row[INFO]
        # Find hospital payables. 
        if 'WILL I HAVE TO PAY' in row[SERVICE]:
            payable = row[INFO]
    f.close()

    return oldPdfInfo(OLD_PDF, None, None, issue_date, avail_for, payable, waiting_period, None)
    


def download_pdf(url, dest):
    '''
    This function downloads the pdf given a url
    and saves it to the given destination.
    '''
    pdf = requests.get(url)
    with open(dest, 'wb') as f:
        f.write(pdf.content)


def create_excel(destination):
    '''
    Sets up Excel Category Sheet & Bold title given sheetname
    '''
    wb = Workbook()
    ws = wb.active
    colname = ["PDF Type", "Name", "Fund", "PDFLink", "Status", "Excess", \
            "Monthly Premium", "State", "Adults", "Scale (Adults + Dependants)", \
            "Availability", "Policy Type", "Corporate Product", \
            "Hospital Cover During Visit", "Hospital Services not Covered", \
            "Hospital Services Limited Cover", "Waiting periods", "Copayment", \
            "Other Hospital Cover Features", "General Dental - WP", \
            "General Dental - Limits", "General Dental - Max Benefits", \
            "Major Dental - WP", "Major Dental - Limits", "Major Dental - Max Benefits", \
            "Endodontic - WP", "Endodontic - Limits", "Endodontic - Max Benefits", \
            "Orthodontic - WP", "Orthodontic - Limits", "Orthodontic - Max Benefits", \
            "Optical - WP", "Optical - Limits", "Optical - Max Benefits", \
            "NonPBSPharmaceuticals - WP", "NonPBSPharmaceuticals - Limits", \
            "NonPBSPharmaceuticals - Max Benefits", "Physio - WP", "Physio - Limits", \
            "Physio - Max Benefits", "Chiropractic - WP", "Chiropractic - Limits", \
            "Chiropractic - Max Benefits", "Podiatry - WP", "Podiatry - Limits", \
            "Podiatry - Max Benefits", "Psychology - WP", "Psychology - Limits", \
            "Psychology - Max Benefits", "Acupuncture - WP", "Acupuncture - Limits", \
            "Acupuncture - Max Benefits", "Naturopathy - WP", "Naturopathy - Limits", \
            "Naturopathy - Max Benefits", "Massage - WP", "Massage - Limits", \
            "Massage - Max Benefits", "HearingAids - WP", "HearingAids - Limits", \
            "HearingAids - Max Benefits", "BloodGlucose Monitoring - WP", \
            "BloodGlucose Monitoring - Limits", "BloodGlucose Monitoring - Max Benefits", \
            "Audiology - WP", "Audiology - Limits", "Audiology - Max Benefits", \
            "Ante-natal/Post-natal - WP", "Ante-natal/Post-natal - Limits", "Ante-natal/Post-natal - Max Benefits", \
            "Chinese Medicine - WP", "Chinese Medicine - Limits", "Chinese Medicine - Max Benefits", \
            "Dietary Advice - WP", "Dietary Advice - Limits", "Dietary Advice - Max Benefits", \
            "Exercise Physiology - WP", "Exercise Physiology - Limits", "Audiology - Max Benefits", \
            "Eye Therapy - Emergency", "Eye Therapy - Call out fees", "Eye Therapy - other information", \
            "Health Management - WP", "Health Management - Limits", "Health Management - Max Benefits", \
            "Home nursing - WP", "Home nursing - Limits", "Home nursing - Max Benefits", \
            "Occupational therapy - WP", "Occupational therapy - Limits", "Occupational therapy - Max Benefits", \
            "Orthotics - WP", "Orthotics - Limits", "Orthotics - Max Benefits", \
            "Osteopathy - WP", "Osteopathy - Limits", "Osteopathy - Max Benefits", \
            "Speech Therapy - WP", "Speech Therapy - Limits", "Speech Therapy - Max Benefits", \
            "Vaccinations - WP", "Vaccinations - Limits", "Vaccinations - Max Benefits", \
            "Ambulance - Emergency", "Ambulance - Call Out Fees", "Ambulance - Other", \
            "Other Treatment Cover Features", "Medicare Surcharge Levy", "Issue Date", \
            "Available for", "Provider Arrangements", "Youth discount", \
            "Travel and accommodation beneft", "Policy ID", "Accident cover"]

    #Creates Bold Column Titles
    for i in range(len(colname)):
        ws.cell(row = 1, column = i + 1).value = colname[i]
        ws.cell(row = 1, column = i + 1).font = Font(size = 14, bold = True)
    wb.save(filename=destination)


def pdf_to_text(path):
    '''
    Converts the pdf into text. Taken from online.
    Source can be found in scraperConst.py as
    PDF_TO_TEXT_SRC.
    '''
    manager = PDFResourceManager()
    retstr = BytesIO()
    layout = LAParams(all_texts=True)
    device = TextConverter(manager, retstr, laparams=layout)
    filepath = open(path, 'rb')
    interpreter = PDFPageInterpreter(manager, device)

    for page in PDFPage.get_pages(filepath, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    filepath.close()
    device.close()
    retstr.close()
    return text.decode('utf-8')


def get_pdf_type(pdf_text):
    '''
    There are 2 types of PDF: the old, and the new.
    This function returns OLD_PDF for old ones, and 
    NEW_PDF for new ones.
    '''
    print(type(pdf_text))
    if OLD_TITLE in pdf_text:
        return OLD_PDF
    elif NEW_TITLE in pdf_text:
        return NEW_PDF


if __name__ == "__main__":
    text = pdf_to_text(r"temp/NJKD20.pdf")
    print(text)
    # scrape_new_pdf(text)
    crit = Criteria("000000")
    web_policy = WebPolicy("ACA", "Gold Deluxe Hospital", "link", "Open", crit, "100", "no excess", "no copay", "no age disc", "No medicare", "No", "no", ["a", 'b'], ['c', 'd'], ['e', 'f'], "other", "J20")
    pdf_info = scrape_old_pdf(text)

    # Creates excel sheet.
    line = "000000"
    sheet = "results.xlsx"
    create_excel(sheet)
    wb = load_workbook(sheet)
    ws = wb.active
    old_populate_excel(web_policy, pdf_info, ws, 2)
    wb.save(sheet)