import sqlite3
import random
from simulator import Simulator

# Connect to the SQLite database
conn = sqlite3.connect('profiles.db')
c = conn.cursor()

# Get the list of all profile IDs
c.execute("SELECT id FROM profiles")
all_profile_ids = [row[0] for row in c.fetchall()]

# Select a random user profile ID
user_profile_id = random.choice(all_profile_ids)

# Select 100 random profiles excluding the user profile
other_profiles = random.sample([id for id in all_profile_ids if id != user_profile_id], 100)

# Close the connection
conn.close()

# Process the user profile
print(f"User profile ID: {user_profile_id}")

# Process other profiles
for profile_id in other_profiles:
    # Fetch the profile details from the database
    conn = sqlite3.connect('profiles.db')
    c = conn.cursor()
    c.execute("SELECT * FROM profiles WHERE id=?", (profile_id,))
    row = c.fetchone()
    if row:
        # Process the profile data as needed
        print(f"Profile ID: {row[0]}, Age: {row[1]}, Religion: {row[2]}, Location: {row[3]}, Zodiac: {row[4]}, Education Level: {row[5]}, Preferences: {row[6]}, Tags: {row[7]}")
    conn.close()

# Initialize the simulator
accepts, rejects = Simulator(user_profile_id, other_profiles)
print(accepts, rejects)