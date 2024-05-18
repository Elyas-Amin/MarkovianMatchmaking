import numpy as np
import uuid
import sqlite3
import json
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq

from Profile import Profile
import prof_char as p_char

def generate_profile():
    id = str(uuid.uuid4())  # Convert UUID to string
    age = int(np.random.normal(30, 5))
    while age < 18: # Ensure age is > 18
        age = int(np.random.normal(30, 5)) 
    religion = p_char.r[np.random.randint(len(p_char.r))-1]
    location = p_char.l[np.random.randint(len(p_char.l))-1]
    zodiac = p_char.z[np.random.randint(len(p_char.z))-1]
    education_level = p_char.e[np.random.randint(len(p_char.e))-1]

    # Add random tags
    tags_to_add = set()
    for i in range(np.random.randint(4, 11)):
        tag = p_char.t[np.random.randint(len(p_char.t)-1)]
        while tag in tags_to_add: # Ensure no repeat tags
            tag = p_char.t[np.random.randint(len(p_char.t)-1)]
        tags_to_add.add(tag)
    
    #add random zodiacs
    zodiacs_to_add = set()
    for i in range(np.random.randint(len(p_char.z))):
        z = p_char.z[np.random.randint(len(p_char.z)-1)]
        while z in zodiacs_to_add: # Ensure no repeat zodiacs
            z = p_char.z[np.random.randint(len(p_char.z)-1)]
        zodiacs_to_add.add(z)


    #should this be expanded?
    preferences = {
        "age_range": 5 + abs(int(np.random.normal(0,8))),
        "religion_pref": p_char.r_pref[np.random.randint(len(p_char.r_pref))-1],
        "zodiac_pref": zodiacs_to_add,
        "education_pref": p_char.e[np.random.randint(len(p_char.e)-1)::]
    }

    threshold = np.random.beta(5, 3, size=None) # Generate acceptance threshold

    #create profile object
    p = Profile(id, age, religion, location, zodiac, education_level, tags_to_add, preferences, threshold)

    return p

def generate_database(size):
    profiles_dict = []
    for x in range(size):
        p = generate_profile()
        profiles_dict.append(p.to_dict())
        
    df = pd.DataFrame(profiles_dict)
    # Explicitly cast columns to correct types
    table = pa.Table.from_pandas(df)
    pq.write_table(table, "profiles.parquet")
    
#Example usage
generate_database(1000000)

# for _ in range(50):
#     print(generate_profile())