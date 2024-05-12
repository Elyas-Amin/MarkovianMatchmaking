from Profile import Profile

global TOTAL_USERS
TOTAL_USERS = 1000

class CSP:
    def __init__(self):
        self.variables - {}
        self.values = {}
        

def isComplete(assigment):
    return len(assigment) == TOTAL_USERS
        
def isConsistent(profiles, value, assignment, var):
    #check if the compatability scores are within a certain range
    if var.compute_compatibility(value) >= 0.5:
        return True
    return False

# def mrv(users):
#     #Choose profile with least amount of prefernecs
#     min = users[0]
#     for x in users:
#         if len(x.prefernces) < len(min.prefernces):
#             min = x
#     return min
    
# def forward_checking(csp):
#     """if domain becomes < 10, return failure"""
#   check cluster size
    
#check to see if fc is necessary for csp's

#
    
def backtracking_search(profiles):
    assigment = {}
    return backtracking(assigment, profiles)

def constraint_acquisition(csp):
    """if one user rejects a profile, this will update the rejected profile's domain as necessary"""
    #constraint acquistion??
    #something here
    

def csp(profile):
    """Variables are each user, constraints are True/False and thresholds for heuristics"""
    
    
def backtracking(assigment, profiles):
    """if forward checking returns failure, update constraint thresholds"""
    if isComplete(assigment):
        return assigment
    var = mrv(assigment, profiles) #choose next user
    for value in var:
        if isConsistent(profiles, value, assigment, var): #if not consistent then remove profile
            if var in assigment.keys():
                assigment[var].append(value) #add new value to list
            else: #createa a new entry with list value containing the profile to be added
                assigment[var] = [value]
            inferences = forward_checking(profiles, assigment, var, value)
            if inferences:
                result = backtracking(assigment, profiles)
                if result:
                    return result
            del assigment[var].remove(value)
    return False
