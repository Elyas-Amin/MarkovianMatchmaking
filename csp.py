from Profile import Profile
from simulator import Simulator
from retriever import Retriever
import pandas as pd
import sqlite3
import json
import random
import timeit
import time

START_TIME = 0
STOP_TIME = 0
START_TIME2 = 0
STOP_TIME2 = 0

class CSP:
    def __init__(self):
        self.variables = {}
        self.values = {}
    
    def isConsistent(self, user, var, var_constraints, potential_match): #checks if the preferences of user matches the characteristics of potential match
        if var == "age_range":
            return (abs(user.age - potential_match.age) <= var_constraints)
        elif var == "religion_pref":
            return potential_match.religion in var_constraints
        elif var == "zodiac_pref":
            return potential_match.zodiac in var_constraints if not potential_match.preferences["zodiac_pref"]  else True
        elif var == "education_pref":
            return potential_match.education_level in var_constraints if not potential_match.preferences["education_pref"] else True
        elif var == "tag_similarity":
            return False if user.preferences["tag_similarity"] <= 1 else True
        
    def forward_checking(self, user, updated_variables, var, potential_match, user_constraints, profiles):
        if not updated_variables: #base case
            return True
                
        for neighbor_var in updated_variables:
            if neighbor_var == var: #if looking at current variable, skip. Precautiornary because it should have already been removed
                continue
            neighbor_constraints = user_constraints[neighbor_var]
            if not self.isConsistent(user, neighbor_var, neighbor_constraints, potential_match):
                return False
            
        return True

    def match_profiles(self, user, profiles, user_matches):
        constraints = user.preferences

        var_count = 0
        for potential_match in profiles:
            user.tag_overlap(potential_match) #get the tag similarity between user and profile
            self.match_profiles_helper(user, profiles, potential_match, constraints, var_count, user_matches)
        
        return user_matches
  
    
    def match_profiles_helper(self, user, profiles, potential_match, constraints, var_count, matches):
        if var_count == 4: #base case
            return matches
        updated_variables = list(matches.keys())
        for var in matches.keys():
            if len(matches[var]) >= 1 and potential_match in matches[var]:
                continue  # Skip if potential match is already assigned
            var_constraints = constraints[var] #add the potential match to the correct preference match

            updated_variables.remove(var) #remove the current variable that we're testing for forward checking
            if self.isConsistent(user, var, var_constraints, potential_match):
                matches[var].append(potential_match)
                inferences = self.forward_checking(user, updated_variables, var, potential_match, constraints, profiles)
                if inferences:
                    result = self.match_profiles_helper(user, profiles, potential_match, constraints, var_count + 1, matches)
                    if result:
                        return result
                matches[var].remove(potential_match)

        return False

# if __name__ == "__main__":
#     csp = CSP()
#     sim = Simulator()
#     ret = Retriever()
    
#     df = pd.read_parquet("new_york_profiles.parquet")
#     # print(df["id"][1])
#     input_parquet_path = "new_york_profiles.parquet"
#     user = ret.retrieve_profile_by_id(input_parquet_path, "a9724be6-cb70-4154-b41d-bd759ce2e00a")
#     profiles = ret.random_profile_chooser(user, input_parquet_path, 100) #takes about 7 seconds
#     user_matches = {
#             "age_range": [],
#             "zodiac_pref": [],
#             "education_pref": [],
#             "tag_similarity" : []
#         }
#     #make sure user not in profiles
#     while user in profiles:
#         user = ret.retrieve_by_location("New York", 1)[0]
#     print(user)
#     profile_copy = profiles.copy()
#     START_TIME = timeit.default_timer()
#     matches = csp.match_profiles(user, profile_copy, user_matches)
#     STOP_TIME = timeit.default_timer()
#     match_set = set() #storing the matches
#     for var, profs in matches.items():
#         for p in profs:
#             if p not in match_set:
#                 match_set.add(p)
#     print("match_set:", len(match_set))
#     print("CSP Run Time(s):", STOP_TIME-START_TIME)

#     #Run Simulation
#     START_TIME2 = timeit.default_timer()
#     simulation_test = sim.simulation(user, match_set)
#     STOP_TIME2 = timeit.default_timer()
#     print("Simulation Run Time(s):", STOP_TIME2-START_TIME2)
#     sum_total = len(simulation_test[0]) + len(simulation_test[1])
#     print(round(len(simulation_test[0])/sum_total, 3), round(len(simulation_test[1])/sum_total, 3))
#     # print("RUNNING TIME:", simulation_test[2])
    




