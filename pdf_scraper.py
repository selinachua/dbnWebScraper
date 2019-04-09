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
from openpyxl import Workbook
from openpyxl.styles import Font
import requests, datetime, re, tabula, sys, csv

from constants import *
from policy import pdfHospPolicy
from service import Service


def scrape_all_pdfs(pdf_dict, sheet):
    '''
    This function is the main pdf_scraper function. It iterates 
    through all the pdfs inside the dictionary and scrapes all
    information into the passed in excel sheet.
    '''
    for fund in pdf_dict:
        pdf_num = 1
        for link in pdf_dict[fund]:
            pdf_dest = TEMP_PDF + fund + str(pdf_num) + ".pdf"
            download_pdf(link, pdf_dest)
            scrape_pdf(pdf_dest)
            pdf_num += 1
            break
        break

    # Clean up temp folder using shutil.rmtree()


def scrape_pdf(pdf_dest):
    '''
    This function scrapes the pdf according to its type.
    '''
    pdf_text = pdf_to_text(pdf_dest)
    pdf_type = get_pdf_type(pdf_text)
    
    if pdf_type == NEW_PDF:
        scrape_new_pdf(pdf_text)
    elif pdf_type == OLD_PDF:
        scrape_old_pdf(pdf_text)
    else:
        print("Couldn't identify PDF type.")


def scrape_new_pdf(pdf_text):
    print("Scraping new pdf...")
    # p = pdfHospPolicy(NEW_PDF)
    tables = tabula.read_pdf(f"{sys.path[0]}/temp/ACA1.pdf", pages=2, flavor='lattice')
    print(tables)
    tabula.convert_into(f"{sys.path[0]}/temp/ACA1.pdf", TEMP_CSV, multiple_tables=True, spreadsheet=True, pages=[1,2], output_format='csv', encoding='utf-8')
    exit(1)



def scrape_old_pdf(pdf_text):
    '''
    This function scrapes the old pdf for wanted information.
    '''
    print("Scraping old pdf...")

    issue_date = ""; avail_for = ""
    waiting_period = ""; payable = ""
    read_hosp_page_old_pdf(pdf_text, issue_date, avail_for, waiting_period, payable)
    read_general_old_pdf(pdf_text)
    


def read_general_old_pdf(pdf_text):
    '''
    This functions reads the general treatment page in the old pdf.
    '''
    # Converts the general table in PDF into CSV format. 
    tabula.convert_into(f"{sys.path[0]}/temp/NAWT20.pdf", TEMP_CSV, \
        lattice=True, spreadsheet=True, pages=2, output_format='csv')

    f = open(TEMP_CSV)
    csv_f = csv.reader(f)

    for row in csv_f:
        # Special cases:
        if 'PROVIDER ARRANGEMENTS:' in row[SERVICE]:
            print("FOUND PROVIDER:", row[SERVICE])
            continue
        elif 'FEATURES' in row[SERVICE] \
            or 'SERVICES' in row[SERVICE] \
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

    f.close()



def read_hosp_page_old_pdf(pdf_text, issue_date, avail_for, waiting_period, payable):
    '''
    This function reads the hospital page in the pdf and scrapes 
    for its issue date and available for.
    '''
    # Grabs issue date.
    issue_date = re.search(r'issued (.*)\n', pdf_text)
    if issue_date:
        print(f"ISSUE DATE: {issue_date.group(1)}")
    else:
        print ("Couldn't find issue date.")
    # Grabs available for information.
    first_lines = pdf_text.rsplit('\n')
    avail_for = ""
    for line in first_lines:
        if 'Residents' in line:
            avail_for = line
            break
    if avail_for:
        print(f"AVAIL FOR: {avail_for}")
    else:
        print("Couldn't find avail for.")
    
    # Read rest of hospital page.
    tabula.convert_into(f"{sys.path[0]}/temp/NAWT20.pdf", TEMP_CSV, \
        lattice=True, spreadsheet=True, pages=1, output_format='csv')

    f = open(TEMP_CSV)
    csv_f = csv.reader(f)

    for row in csv_f:
        # Find waiting period.
        if 'HOW LONG ARE THE WAITING' in row[SERVICE]:
            waiting_period = row[INFO]
        # Find hospital payables. 
        if 'WILL I HAVE TO PAY' in row[SERVICE]:
            payable = row[INFO]
    f.close()
        


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
    colname = ["Name", "Fund", "PDFLink", "Status", "Excess", \
            "Monthly Premium", "State", "Adults", "Dependants", \
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
            "Ambulance - Emergency", "Ambulance - Call out fees", "Ambulance - other information", \
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
    text = pdf_to_text(r"temp/NAWT20.pdf")
    # print(text)
    # scrape_new_pdf(text)
    scrape_old_pdf(text)
    


    # # Creates excel sheet.
    # line = "000000"
    # sheet = EXCEL_SHEET + "Criteria " + line + " " + \
    #         datetime.datetime.now().strftime("%d %B %Y at %H.%M") + ".xlsx"
    # create_excel(sheet)
    # dest = sheet
    # pdf_url = "https://www.privatehealth.gov.au/dynamic/Download/ACA/J8/A0000C"
    # download_pdf(pdf_url, TEMP_PDF)
    # # text = pdf_to_text(r"PDF_examples/A0000C.pdf")
    # # print(text.decode('utf-8'))

    # # create_excel(EXCEL_SHEET + "res.xlsx")