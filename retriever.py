import sqlite3
import json
import random
from Profile import Profile

class Retriever:

    def random_profiles(self, n):
        # Connect to the SQLite database
        conn = sqlite3.connect('profiles.db')
        c = conn.cursor()

        # Get the list of all profile IDs
        c.execute("SELECT id FROM profiles")
        all_profile_ids = [row[0] for row in c.fetchall()]

        # Select a random user profile ID
        user_profile_id = random.choice(all_profile_ids)

        # Select n random profiles excluding the user profile
        other_profiles = random.sample([id for id in all_profile_ids if id != user_profile_id], n)

        # Fetch the user profile
        c.execute("SELECT * FROM profiles WHERE id=?", (user_profile_id,))
        user_row = c.fetchone()

        # Parse the preferences column from JSON to dictionary
        user_preferences = json.loads(user_row[6])

        # Create a Profile instance for the user
        user = Profile(user_row[0], user_row[1], user_row[2], user_row[3], user_row[4], user_row[5], user_preferences)

        # Fetch the other profiles and convert them to Profile instances
        other_profiles_instances = []
        for profile_id in other_profiles:
            c.execute("SELECT * FROM profiles WHERE id=?", (profile_id,))
            profile_row = c.fetchone()
            preferences = json.loads(profile_row[6])
            p = Profile(profile_row[0], profile_row[1], profile_row[2], profile_row[3], profile_row[4], profile_row[5], preferences)
            other_profiles_instances.append(p)

        # Close the connection
        conn.close()

        return user, other_profiles_instances
    
def first_profiles(self, n):
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()

    # Select first n profiles excluding the user profile
    c.execute("SELECT * FROM profiles ORDER BY id LIMIT %s" % n)
    first_profiles = c.fetchall()

    profiles = []
    for profile_tuple in first_profiles:
        profile_id = profile_tuple[0]  # Extracting the id from the tuple
        c.execute("SELECT * FROM profiles WHERE id=?", [profile_id])
        profile_row = c.fetchone()
        preferences = json.loads(profile_row[6])
        p = Profile(profile_row[0], profile_row[1], profile_row[2], profile_row[3], profile_row[4], profile_row[5], preferences)
        profiles.append(p)

    conn.close()

    return profiles