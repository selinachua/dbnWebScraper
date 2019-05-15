class NewPDFInfo():
    def __init__(self, pdf_type, hosp, general, ambulance):
        self.pdf_type = pdf_type
        self.hosp = hosp
        self.services = general
        self.ambulance = ambulance 
    def __str__(self):
        string = (
            f"PDF Type: {self.pdf_type}\n"
        )
        string += self.hosp.__str__()
        string += self.ambulance.__str__()
        for s in self.services:
            string += self.services[s].__str__() + '\n'
        return string


class NewHospInfo():
    def __init__(self, wait, avail, avail_for, travel_ben, accident_cover, \
                 prov_arr, issue_date, gen_other, hosp_other):
        self.wait = wait
        self.avail = avail
        self.avail_for = avail_for
        self.travel_ben = travel_ben
        self.accident_cover = accident_cover
        self.prov_arr = prov_arr
        self.issue_date = issue_date
        self.general_other = gen_other
        self.hosp_other = hosp_other
    def __str__(self):
        string = (
            f"Wait: {self.wait}\n"
            f"Avail: {self.avail}\n"
            f"Available For: {self.avail_for}\n"
            f"Travel Benefits: {self.travel_ben}\n"
            f"Accident Cover: {self.accident_cover}\n"
            f"Provider Arrangements: {self.prov_arr}\n"
            f"Issue Date: {self.issue_date}\n"
            f"General other: {self.general_other}\n"
            f"Hospital other: {self.hosp_other}\n"
        )
        return string

class AmbulanceInfo():
    def __init__(self, emer, callout, other):
        self.emer = emer
        self.callout = callout
        self.other = other
    def __str__(self):
        string = (
            f"Emergency: {self.emer}\n"
            f"Call-Out Fee: {self.callout}\n"
            f"Other: {self.other}\n"
        )
        return string