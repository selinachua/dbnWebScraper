'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains the policy class.
# This class will contain everything that needs to be
# populated for the excel spread sheet.
'''

class pdfPolicy:
    def __init__(self, pol_id):
        self.id = pol_id


class WebPolicy:
    def __init__(self, fund_name, name, status, criteria, premium, excess, co_pay, age_disc,
                    medicare, hosp_accom, hosp_tier, covered, not_covered, limited_cover,
                    other_hosp_feature, pol_id):
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
        self.covered = covered
        self.not_covered = not_covered
        self.limited_cover = limited_cover
        self.other_hosp_feature = other_hosp_feature
        self.id = pol_id

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
            f"Covered: {self.covered}\n"
            f"Not Covered: {self.not_covered}\n"
            f"Limited Cover: {self.limited_cover}\n"
            f"Other Hosptial Features: {self.other_hosp_feature}\n"
            f"Policy ID: {self.id}"
        )
        string += self.criteria.__str__()
        return string


