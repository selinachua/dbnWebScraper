'''
# Created by:
# Selina Chua
# selina.a.chua@gmail.com
#
# This file contains a class that stores information
# for general services.
'''

class Service():
    def __init__(self, name, cover, wait, limits, max_benefits):
        self.name = name
        self.cover = cover
        self.wait = wait
        self.limits = limits
        self.max_benefits = max_benefits

    def __str__(self):
        string = (
            f"--- {self.name} ---\n"
            f"Cover: {self.cover}\n"
            f"Waiting Period: {self.wait}\n"
            f"Benefit Limits: {self.limits}\n"
            f"Max Benefits: {self.max_benefits}\n" 
        )
        return string