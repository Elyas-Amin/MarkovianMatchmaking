import numpy as np
import uuid
import sqlite3
import json

from Profile import Profile
import prof_char as p_char

def generate_profile(religions, locations, zodiac_signs, education_levels, tags):
    id = str(uuid.uuid4())  # Convert UUID to string
    age = np.random.randint(18, 100)
    religion = religions[np.random.randint(len(religions))]
    location = locations[np.random.randint(len(locations))]
    zodiac = zodiac_signs[np.random.randint(len(zodiac_signs))]
    education_level = education_levels[np.random.randint(len(education_levels))]

    preferences = {
        "age_range": np.random.randint(1, 50),
        "religion_pref": p_char.r_pref[np.random.randint(len(p_char.r_pref))],
        "zodiac_pref": [zodiac_signs[i] for i in np.random.randint(len(zodiac_signs), size=np.random.randint(len(zodiac_signs)))],
        "education_pref": [education_levels[i] for i in np.random.randint(len(education_levels), size=np.random.randint(len(education_levels)))]
    }

    p = Profile(id, age, religion, location, zodiac, education_level, preferences)

    # Add random tags
    for i in range(np.random.randint(len(tags))):
        p.tags.add(tags[np.random.randint(1, 10)])

    return p


def generate_database(size):
    # Connect to the SQLite database
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()

    # Create a table to store the profiles
    c.execute('''CREATE TABLE IF NOT EXISTS profiles
                 (id TEXT, age INTEGER, religion TEXT, location TEXT, zodiac TEXT, education_level TEXT, preferences TEXT, tags TEXT)''')

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
generate_database(100000)
# print(generate_profile(p_char.r, p_char.l, p_char.z, p_char.e, p_char.t))