import random
import pandas as pd
import pyarrow.parquet as pq

class Retriever:

    def retrieve_by_location(city, n):
        # Read the Parquet file into a DataFrame
        table = pq.read_table('profiles.parquet')
        df = table.to_pandas()
        
        # Filter profiles by the specified city
        city_profiles = df[df['location'] == city]
        
        # Ensure that there are enough profiles for the specified city
        if len(city_profiles) < n:
            print(f"There are only {len(city_profiles)} profiles available for {city}.")
            return None
        
        # Randomly select n profiles from the filtered DataFrame
        selected_profiles = random.sample(city_profiles.index.tolist(), n)
        
        # Retrieve the selected profiles
        selected_data = city_profiles.loc[selected_profiles]
        
        return selected_data
    
    print(retrieve_by_location("Philadelphia", 10000))