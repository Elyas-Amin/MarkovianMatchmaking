from Profile import Profile

global TOTAL_USERS
TOTAL_USERS = 1000

class CSP:
    def __init__(self):
        self.variables - {}
        self.values = {}
        

def isComplete(assigment):
    return len(assigment) == TOTAL_USERS
        

def mrv(users):
    #Choose profile with least amount of prefernecs
    min = users[0]
    for x in users:
        if len(x.prefernces) < len(min.prefernces):
            min = x
    return min
    

def forward_checking(csp):
    """if domain becomes < 10, return failure"""
    
def backtracking_search(profiles):
    assigment = {}
    return backtracking(assigment, profiles)

def backtracking(assigment, profiles):
    """if forward checking returns failure, update constraint thresholds"""
    if isComplete(assigment):
        return assigment
    var = mrv(assigment, profiles) #choose next user
    for value in var:
        if is_consistent(profiles, value, assigment, var):
            assigment[var] = value
            inferences = forward_checking(profiles, assigment, var, value)
            if inferences:
                result = backtracking(assigment, profiles)
                if result:
                    return result
            del assigment[var]
    return False

def ac_3(csp):
    """if one user rejects a profile, this will update the rejected profile's domain as necessary"""
    #constraint acquistion??
    #something here
    

def csp(profile):
    """Variables are each user, constraints are True/False and thresholds for heuristics"""