from Profile import Profile
from simulator import Simulator
import sqlite3
import json
import random
import timeit
import time

START_TIME = 0
STOP_TIME = 0

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
        # elif var == "tag_similarity":
        #     print(user.preferences["tag_similarity"])
        #     return False if user.preferences["tag_similarity"] <= 0 else True
        

    def forward_checking(self, user, variables, var, potential_match, constraints, profiles):
        #What is the base case?
        if not variables:
            return True
                
        for neighbor in variables:
            if neighbor == var:
                continue
            neighbor_constraints = constraints[neighbor]
            if not self.isConsistent(user, neighbor, neighbor_constraints, potential_match):
                return False
            
        return True

    def match_profiles(self, user, profiles, user_matches):
        constraints = user.preferences

        var_count = 0
        for potential_match in profiles:
            user.tag_overlap(potential_match)
            self.match_profiles_helper(user, profiles, potential_match, constraints, var_count, user_matches)
        
        return user_matches
  
    
    def match_profiles_helper(self, user, profiles, potential_match, constraints, var_count, matches):
        if var_count == 3: #base case
            return matches
        variables = matches.keys()
        updated_variables = list(matches.keys())
        for var in matches.keys():
            if len(matches[var]) >= 1 and potential_match in matches[var]:
                continue  # Skip if potential match is already assigned
            var_constraints = constraints[var]

            updated_variables.remove(var)
            if self.isConsistent(user, var, var_constraints, potential_match):
                matches[var].append(potential_match)
                inferences = self.forward_checking(user, updated_variables, var, potential_match, constraints, profiles)
                if inferences:
                    result = self.match_profiles_helper(user, profiles, potential_match, constraints, var_count + 1, matches)
                    if result:
                        return result
                matches[var].remove(potential_match)

        return False


if __name__ == "__main__":
    csp = CSP()
    sim = Simulator()

    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()

    # c.execute("SELECT id FROM profiles")
    # all_profile_ids = [row[0] for row in c.fetchall()]

    # Select 1000 random profiles excluding the user profile
    # random_profiles = random.sample([id for id in all_profile_ids], 1000)


    START_TIME = timeit.default_timer()
    c.execute("SELECT * FROM profiles ORDER BY id LIMIT 100")
    random_profiles = c.fetchall()

    profiles = []
    counter1 =0
    for profile_tuple in random_profiles:
        profile_id = profile_tuple[0]  # Extracting the id from the tuple
        c.execute("SELECT * FROM profiles WHERE id=?", [profile_id])
        profile_row = c.fetchone()
        preferences = json.loads(profile_row[6])
        profile_instance = Profile(profile_row[0], profile_row[1], profile_row[2], profile_row[3], profile_row[4], profile_row[5], preferences)
        profiles.append(profile_instance)
        counter1+=1
        print(counter1)

    conn.close()

    matches = {}

    counter = 0
    for user in profiles:
        user_matches = {
            "age_range": [],
            # "religion_pref": [],
            "zodiac_pref": [],
            "education_pref": [],
            # "tag_similarity" : []
        }
        profile_copy = profiles.copy()
        profile_copy.remove(user)
        matches[user] = csp.match_profiles(user, profile_copy, user_matches)
        print(user.preferences)
        counter+=1
        print(counter)
    STOP_TIME = timeit.default_timer()

    final_matches = {}

    for user, var_dict in matches.items():
        count = 0
        if type(var_dict) == bool:
            print(user.id, 0)
            continue
        match_set = set()
        for var, profiles in var_dict.items():
            for p in profiles:
                if p not in match_set:
                    match_set.add(p)
        # print(match_set)
        final_matches[user] = match_set
        simulation_test = sim.simulation(user, match_set)
        sum_total = len(simulation_test[0]) + len(simulation_test[1])
        print(round(len(simulation_test[0])/sum_total, 3), round(len(simulation_test[1])/sum_total, 3))
        # print(user.id, len(match_set))
    

    
    print(STOP_TIME-START_TIME)




