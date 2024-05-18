import sqlite3
import random
import json
from generator import generate_profile
from simulator import Simulator
from Profile import Profile
from csp import CSP
from drl import DQNAgent

# # Connect to the SQLite database
# conn = sqlite3.connect('profiles.db')
# c = conn.cursor()

# # Get the list of all profile IDs
# c.execute("SELECT id FROM profiles")
# all_profile_ids = [row[0] for row in c.fetchall()]

# # Select a random user profile ID
# user_profile_id = random.choice(all_profile_ids)

# # Select 100 random profiles excluding the user profile
# other_profiles = random.sample([id for id in all_profile_ids if id != user_profile_id], 1000)

# # Fetch the user profile
# c.execute("SELECT * FROM profiles WHERE id=?", (user_profile_id,))
# user_row = c.fetchone()

# # Parse the preferences column from JSON to dictionary
# preferences = json.loads(user_row[6])  # Assuming preferences is the 7th column (index 6)

# # Create a Profile instance for the user
# user_profile = Profile(user_row[0], user_row[1], user_row[2], user_row[3], user_row[4], user_row[5], preferences)

# # Fetch the other profiles and convert them to Profile instances
# other_profiles_instances = []
# for profile_id in other_profiles:
#     c.execute("SELECT * FROM profiles WHERE id=?", (profile_id,))
#     profile_row = c.fetchone()
#     preferences = json.loads(profile_row[6])
#     profile_instance = Profile(profile_row[0], profile_row[1], profile_row[2], profile_row[3], profile_row[4], profile_row[5], preferences)
#     other_profiles_instances.append(profile_instance)

# # Close the connection
# conn.close()

user_profile = generate_profile()
other_profiles_instances = []

num = 1000
for _ in range(num):
    other_profiles_instances.append(generate_profile())

csp = CSP()

user_matches = {
    "age_range": [],
    "zodiac_pref": [],
    "education_pref": [],
    "tag_similarity" : []
}

matches = csp.match_profiles(user_profile, other_profiles_instances, user_matches)
match_set = set()
for var, profiles in matches.items():
    for p in profiles:
        if p not in match_set:
            match_set.add(p)


# Initialize the simulator
simulation = Simulator()
agent = DQNAgent()

# Simulate the user's decisions
rand_accepts, rand_rejects = simulation.simulation(user_profile, other_profiles_instances)
csp_accepts, csp_rejects = simulation.simulation(user_profile, list(match_set))
drl_accepts, drl_suggested = agent.unsupervised_learning(user_profile, other_profiles_instances, simulation)

print(user_profile)
# print(len(match_set))
print(len(rand_accepts)/num)
print(len(csp_accepts)/len(match_set))
print(drl_accepts/drl_suggested)


