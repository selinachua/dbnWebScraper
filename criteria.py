'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains the criteria class. 
'''

class Criteria():
    def __init__(self, criteria):
        self.state = int(criteria[0])
        self.adults = int(criteria[1])
        self.dpndnts = int(criteria[2])
        self.pol_type = int(criteria[3])
        self.status = int(criteria[4])
        self.corp = int(criteria[5])

    def __str__(self):
        string = (
            f"- CRITERIA -\n"
            f"State: {self.state}\n"
            f"Adults: {self.adults}\n"
            f"Dependants: {self.dpndnts}\n"
            f"Policy Type: {self.pol_type}\n"
            f"Status: {self.status}\n"
            f"Corporate: {self.corp}\n"
        )
        return string