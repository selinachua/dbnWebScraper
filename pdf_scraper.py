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

from constants import *

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
    return text


def get_pdf_type(pdf_text):
    '''
    There are 2 types of PDF: the old, and the new.
    This function returns OLD_PDF for old ones, and 
    NEW_PDF for new ones.
    '''
    if OLD_TITLE in pdf_text:
        return OLD_PDF
    elif NEW_TITLE in pdf_text:
        return NEW_PDF


if __name__ == "__main__":
    text = pdf_to_text(r"A0000S.pdf")
    print(text.decode('utf-8'))
    print("\n\n")
    text2 = pdf_to_text(r"NIZV10.pdf")
    print("OLDER PDF \n", text2.decode('utf-8'))