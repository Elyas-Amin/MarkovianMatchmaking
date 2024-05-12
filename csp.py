from Profile import Profile

global TOTAL_USERS
TOTAL_USERS = 1000

class CSP:
    def __init__(self):
        self.variables - {}
        self.values = {}

    # def isComplete(assigment):
    #     return len(assigment) == TOTAL_USERS
            
    def isConsistent(self, user, var, constraints[var], potential_match):
        #in backtracking relax the constraints
        if var == "age": #age constraint should be single number
            if abs(user.age - potential_match.age) <= constraints[var]:
                return True
        elif var == "religion":
            if potential_match.va not in constraints[var]:
                return False
            return True
        elif var == "location":
            if potential_match.location not in constraints[var]:
                return False
            return True
        elif var == "zodiac":
            if potential_match.zodiac not in constraints[var]:
                return False
            return True
        elif var == "education_level":
            if potential_match.education_level not in constraints[var]:
                return False
            return True            
        
        
    def forward_checking(self, user, variables, var, potential_match, constraints, generated_profiles):
        remaining_profiles = generated_profiles.copy() #not sure if needed, ask jeffrey
        remaining_profiles.remove(potential_match) #remove current match
        
        if remaining_profiles < 10:
            return False
        
        for neighbor in variables:
            if neighbor == var: #skip current var
                continue
            #check if other var will reduce the overall remaining profiles to less than 10
            if not self.isConsistent(user, neighbor, constraints[neighbor], potential_match):
                return False
        return True

    def constraint_acquisition(csp):
        """if one user rejects a profile, this will update the rejected profile's domain as necessary"""
        #constraint acquistion??
        #something here
        
    def match_profiles(self, user, generated_profiles, matches = {}):
                
        variables = user.preferences.keys()
        domain = generated_profiles.copy() #not sure if needed, ask jeffrey
        domain.remove(user)
        constraints = user.prefernces.copy() #not sure if needed, ask jeffrey
            
        for var in variables:
            matches[var] = []    
                
        for potential_match in generated_profiles:
            for var in variables: #choose next characteristic to match
                if self.isConsistent(user, var, constraints[var], potential_match):
                    matches[var].append(potential_match) #don't need to reduce domain, just add to matches
                    inferences = self.forward_checking(user, variables, var, potential_match, constraints[var], generated_profiles)
                    if inferences:
                        result = match_profiles(user, domain, matches)
                        if result:
                            return result
                    matches[var].remove(potential_match) #remove current assigment in fc fails
            return False


#########################################################################

def __main__(self):
    generated_profiles = #call on profile generator here
    
    matches = {}
    
    for user in generated_profiles:
        matches[user] = self.match_profiles(user, generated_profiles)
    
    return matches
    