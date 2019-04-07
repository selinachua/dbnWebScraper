'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains the policy class.
# This class will contain everything that needs to be
# populated for the excel spread sheet.
'''

class Policy:
    def __init__(self, fund_name, name, status, criteria, premium, excess, co_pay, age_disc,
                    medicare, hosp_accom, hosp_tier):
        self.fund_name = fund_name
        self.name = name
        self.status = status
        self.criteria = criteria
        self.premium = premium
        self.excess = excess
        self.co_pay = co_pay
        self.age_disc = age_disc
        self.medicare = medicare
        self.hosp_accom = hosp_accom
        self.hosp_tier = hosp_tier

    def __str__(self):
        string = (
            f"Fund Name: {self.fund_name}\n"
            f"Policy Name: {self.name}\n"
            f"Status: {self.status}\n"
            f"Premium: {self.premium}\n"
            f"Excess: {self.excess}\n"
            f"Co-payment: {self.co_pay}\n"
            f"Age Discount: {self.age_disc}\n"
            f"Medicare Levy: {self.medicare}\n"
            f"Hospital Accomodation: {self.hosp_accom}\n"
            f"Hospital Tier: {self.hosp_tier}\n"
        )
        string += self.criteria.__str__()
        return string


