import numpy as np
import uuid
import sqlite3
import json
import random

from Profile import Profile
import prof_char as p_char


def non_preferable_age_range(current_age, preference_range):
    # Calculate preferable age range
    lower_bound_preferable = max(18, current_age - preference_range)
    upper_bound_preferable = current_age + preference_range
    
    # Define non-preferable age ranges
    non_preferable_below = 18 if lower_bound_preferable == 18 else lower_bound_preferable - 1
    non_preferable_above = upper_bound_preferable + 1
    
    return (18, non_preferable_below), (non_preferable_above, 'infinity')


def choose_random_non_preferable_age(current_age, preference_range):
    non_preferable_range = non_preferable_age_range(current_age, preference_range)
    below_range = non_preferable_range[0]
    above_range = non_preferable_range[1]

    # Choose a set: below or above
    if below_range[1] >= 18:  # Ensure there is a valid below range
        ranges = ["below", "above"]
    else:
        ranges = ["above"]  # Only above range is valid

    chosen_range = np.random.choice(ranges)

    if chosen_range == "below":
        random_age = np.random.uniform(below_range[0], below_range[1])
    else:
        random_age = np.random.uniform(above_range[0], above_range[0] + 20)  # Set a practical upper limit for random selection
    
    return random_age

def generate_profile(religions, locations, zodiac_signs, education_levels, tags):
    id = str(uuid.uuid4())  # Convert UUID to string
    age = age = int(np.random.normal(30, 5))
    while age < 18: # Ensure age is > 18
        age = int(np.random.normal(30, 5)) 
    religion = religions[np.random.randint(len(religions))]
    location = locations[np.random.randint(len(locations))]
    zodiac = zodiac_signs[np.random.randint(len(zodiac_signs))]
    education_level = education_levels[np.random.randint(len(education_levels))]

    preferences = {
        "age_range": 5 + abs(int(np.random.normal(0,10))),
        "religion_pref": p_char.r_pref[np.random.randint(len(p_char.r_pref))],
        "zodiac_pref": [zodiac_signs[i] for i in np.random.randint(len(zodiac_signs), size=np.random.randint(len(zodiac_signs)))],
        "education_pref": education_levels[np.random.randint(len(education_levels)-1)::]
    }

    p = Profile(id, age, religion, location, zodiac, education_level, preferences)

    # Add random tags
    for i in range(np.random.randint(3, len(tags))):
        p.tags.add(tags[np.random.randint(1, 10)])

    return p

def generate_sim_dis_profile(user, sim_dis: bool):
    #similar profiles: choose random values from preferences of the current user
    if sim_dis:
        id = str(uuid.uuid4()) #random id number value creation
        #if age difference is less than 18 then make minimum 18
        age_min = user.age-user.preferences["age_range"] if user.age-user.preferences["age_range"] >= 18 else 18
        age = np.random.randint(age_min, user.age+user.preferences["age_range"])
        location = user.location
        religion = random.choice(p_char.r) if user.religion == "open to all" else user.religion
        education_level = random.choice(user.preferences["education_pref"]) if user.preferences["education_pref"] else random.choice(p_char.e)
        zodiac =  random.choice(user.preferences["zodiac_pref"]) if user.preferences["zodiac_pref"] else random.choice(p_char.z)
        
        p = Profile(id, age, religion, location, zodiac, education_level, user.preferences)
        
        for i in user.tags:
            ran_num = np.random.random()
            if ran_num >= 0.5:
                p.tags.add(i)
        
        return p
    
    #disimilar profiles: choose random values from preferences of the current user
    elif not sim_dis:
        id = str(uuid.uuid4()) #random id number value creation
        
        age = choose_random_non_preferable_age(user.age, user.preferences["age_pref"])
        location = np.random.choice(p_char.l)
        religion = np.random.choice(p_char.r) 
        education_level = np.random.choice(p_char.e)
        zodiac =  np.random.choice(p_char.z)
        
        p = Profile(id, age, religion, location, zodiac, education_level, user.preferences)
        
        for i in user.tags:
            ran_num = np.random.random(0, 1)
            if ran_num >= 0.5:
                p.tags.add(i)
        
        return p
         
def generate_sim_dis_profile_database(size, user: Profile, sim_dis: bool):
    
    conn = sqlite3.connect('profiles_similar.dp')
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXITS profiles
                 (id TEXT, age INTEGER, religion TEXT, location TEXT, aodiac TEXT, education_level TEXT, preferences TEXT, tags TEXT)''')
    
    for x in range(size):
        #based on current user generate a similar profile
        profile = generate_sim_dis_profile(user, sim_dis)
        # Convert preferences and tags to JSON strings
        preferences_json = json.dumps(profile.preferences)
        tags_json = json.dumps(list(profile.tags))
        c.execute("INSERT INTO profiles (id, age, religion, location, zodiac, education_level, preferences, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (profile.id, profile.age, profile.religion, profile.location, profile.zodiac, profile.education_level, preferences_json, tags_json))
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    

def generate_database(size):
    # Connect to the SQLite database
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()

    # Create a table to store the profiles
    c.execute('''CREATE TABLE IF NOT EXITS profiles
                 (id TEXT, age INTEGER, religion TEXT, location TEXT, aodiac TEXT, education_level TEXT, preferences TEXT, tags TEXT)''')
     
    # Generate and insert profiles into the database
    for x in range(size):
        profile = generate_profile(p_char.r, p_char.l, p_char.z, p_char.e, p_char.t)
        # Convert preferences and tags to JSON strings
        preferences_json = json.dumps(profile.preferences)
        tags_json = json.dumps(list(profile.tags))
        c.execute("INSERT INTO profiles (id, age, religion, location, zodiac, education_level, preferences, tags) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                  (profile.id, profile.age, profile.religion, profile.location, profile.zodiac, profile.education_level, preferences_json, tags_json))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

# Example usage
# generate_database(100000)

# p = generate_profile(p_char.r, p_char.l, p_char.z, p_char.e, p_char.t)
# print(p)
# print("---------------------------")
# print(generate_sim_dis_profile(p, False))

for _ in range(50):
    print(generate_profile(p_char.r, p_char.l, p_char.z, p_char.e, p_char.t))