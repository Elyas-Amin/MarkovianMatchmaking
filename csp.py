from Profile import Profile
import sqlite3
import json
import random

global TOTAL_USERS
TOTAL_USERS = 1000

class CSP:
    def __init__(self):
        self.variables = {}
        self.values = {}

    def isConsistent(self, user, var, var_constraints, potential_match):
        if var == "age_range":
            return abs(user.age - potential_match.age) <= var_constraints
        elif var == "religion_pref":
            return potential_match.religion in var_constraints
        # elif var == "location_pref":
        #     return potential_match.location == var_constraints
        elif var == "zodiac_pref":
            return potential_match.zodiac in var_constraints
        elif var == "education_pref":
            return potential_match.education_level in var_constraints

    def forward_checking(self, user, variables, var, potential_match, constraints, generated_profiles):
        # generated_profiles.remove(potential_match)

        if len(generated_profiles) < 2:
            return False

        for neighbor in variables:
            if neighbor == var:
                continue
            neighbor_constraints = constraints[neighbor]
            if not self.isConsistent(user, neighbor, neighbor_constraints, potential_match):
                return False
            
        # generated_profiles.append(potential_match)
        return True

    def match_profiles(self, user, profiles, var_count, matches):
        constraints = user.preferences

        if var_count == 3:
            return matches

        for potential_match in profiles:
            for var in matches.keys():
                if len(matches[var]) == 1 and potential_match in matches[var]:
                    continue  # Skip if potential match is already assigned
                var_constraints = constraints[var]

                if self.isConsistent(user, var, var_constraints, potential_match):
                    matches[var].append(potential_match)
                    inferences = self.forward_checking(user, matches.keys(), var, potential_match, constraints, profiles)
                    if inferences:
                        result = self.match_profiles(user, profiles, var_count + 1, matches)
                        if result:
                            return result
                    matches[var].remove(potential_match)

        return False


if __name__ == "__main__":
    csp = CSP()

    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()

    # c.execute("SELECT id FROM profiles")
    # all_profile_ids = [row[0] for row in c.fetchall()]

    # Select 1000 random profiles excluding the user profile
    # random_profiles = random.sample([id for id in all_profile_ids], 1000)

    c.execute("SELECT * FROM profiles ORDER BY id LIMIT 10000")
    random_profiles = c.fetchall()

    profiles = []
    for profile_tuple in random_profiles:
        profile_id = profile_tuple[0]  # Extracting the id from the tuple
        c.execute("SELECT * FROM profiles WHERE id=?", [profile_id])
        profile_row = c.fetchone()
        preferences = json.loads(profile_row[6])
        profile_instance = Profile(profile_row[0], profile_row[1], profile_row[2], profile_row[3], profile_row[4], profile_row[5], preferences)
        profiles.append(profile_instance)

    conn.close()

    matches = {}

    for user in profiles:
        user_matches = {
            "age_range": [],
            # "religion_pref": [],
            "zodiac_pref": [],
            "education_pref": []

        }
        var_count = 0
        profile_copy = profiles.copy()
        profile_copy.remove(user)
        matches[user] = csp.match_profiles(user, profile_copy, var_count, user_matches)

        # Printing the result
        for user, match in matches.items():
            if type(match) == bool:
                continue
            # print(len(match["age_range"]))
            match_set = set()
            for var, list in match.items():
                for p in list:
                    if p not in match_set:
                        match_set.add(p)
            
            print(user.id, len(match_set))




