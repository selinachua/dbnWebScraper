'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains the classes used for the old pdf.
'''

class oldPdfInfo():
    def __init__(self, pdf_type, prov_arr, services, issue_date, avail_for, co_pay, wait_period, other):
        self.pdf_type = pdf_type
        self.prov_arr = prov_arr
        self.services = services
        self.issue_date = issue_date
        self.avail_for = avail_for
        self.co_pay = co_pay
        self.wait = wait_period
        self.general_other = other

    def __str__(self):
        string = (
            f"Provider Arrangments = {self.prov_arr}\n"
            f"Issue Date = {self.issue_date}\n"
            f"Available for: {self.avail_for}\n"
            f"Payables = {self.co_pay}\n"
            f"Wait Period = {self.wait}\n"
        )
        string += f"General Services:"
        for s in self.services:
            string += self.services[s].__str__()
        return string