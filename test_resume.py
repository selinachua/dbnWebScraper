from constants import *

def create_all_criteria():
    '''
    Creates all the possible criterias for answering the Step 1 -
    Type of Cover form. 
    '''
    f = open(CRITERIA_FILE, "w+")
    # Cover all criterias in loop
    for state in range(MAX_STATE + 1):
        for adults in range(MAX_ADULTS + 1):
            for dpndnts in range(MAX_DPNDNTS + 1):
                for treatment in range(MAX_TREATMENT + 1):
                    for avail in range(MAX_AVAIL + 1):
                        for corp in range(MAX_CORP + 1):
                            criteria = str(state) + str(adults) + str(dpndnts) + str(treatment) + str(avail) + str(corp)
                            f.write(criteria + "\n")
    f.close()