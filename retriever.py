import random
import pandas as pd
import pyarrow.parquet as pq
from Profile import Profile
from generator import generate_profile
import json

class Retriever:
    
    def retrieve_profile_by_id(self, input_parquet_path, id: str):
        #read in file
        table = pq.read_table(input_parquet_path)
        df = table.to_pandas()
        # id = "740c55d8-b376-46be-929e-04cec6a26531"
        for x in df["id"]:
            if x == id:
                result = df[df["id"] == id]
                break
        
        if result.empty:
            return None

        row = result.iloc[0]
        
        preferences = json.loads(row['preferences'])
        profile = Profile(
            id=str(row['id']),
            age=int(row['age']),
            religion=row['religion'],
            location=row['location'],
            zodiac=row['zodiac'],
            education_level=row['education_level'],
            preferences=preferences,
            tags=set(row['tags']),
            threshold=float(row['threshold'])
        )
        return profile
    
    def retrieve_profile_by_threshold(self, input_parquet_path, threshold):
        # Read in the Parquet file
        table = pq.read_table(input_parquet_path)
        df = table.to_pandas()
        
        # Initialize result to None
        result = None
        
        # Iterate through the 'threshold' column
        for x in df["threshold"]:
            # Check if the rounded value matches the provided threshold
            if round(x, 3) == threshold:
                # Filter the DataFrame based on the threshold value
                result = df[round(df["threshold"], 3) == threshold]
                break
        
        # If no matching rows found, return None
        if result is None or result.empty:
            return None
        
        # Extract the first matching row
        row = result.iloc[0]
        
        # Parse the 'preferences' field from JSON string to a dictionary
        preferences = json.loads(row['preferences'])
        
        # Create and return a Profile object
        profile = Profile(
            id=str(row['id']),
            age=int(row['age']),
            religion=row['religion'],
            location=row['location'],
            zodiac=row['zodiac'],
            education_level=row['education_level'],
            preferences=preferences,
            tags=set(row['tags']),
            threshold=float(row['threshold'])
        )
        
        return profile
        

    def retrieve_by_location(self, city, n, user = None):
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
        
        profiles = []
        for _, row in selected_data.iterrows():
            preferences = json.loads(row['preferences'])
            profile = Profile(
                id=str(row['id']),
                age=int(row['age']),
                religion=row['religion'],
                location=row['location'],
                zodiac=row['zodiac'],
                education_level=row['education_level'],
                preferences=preferences,
                tags=set(row['tags']),
                threshold=float(row['threshold'])
            )
            
        # Ensure the user profile is not included in the retrieved profiles
        if user and profile.id != user.id:
            profiles.append(profile)
        elif not user:
            profiles.append(profile)
        
        return profiles    
    
    def retrieve_every_profile(self, parquet_file_path):
        # Read the Parquet file into a DataFrame
        df = pd.read_parquet(parquet_file_path, engine='pyarrow')
        
        # List to store all Profile objects
        profiles = []

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            # Parse the 'preferences' field from JSON string to a dictionary
            preferences = json.loads(row['preferences'])
            
            # Create a Profile object for the current row
            profile = Profile(
                id=str(row['id']),
                age=int(row['age']),
                religion=row['religion'],
                location=row['location'],
                zodiac=row['zodiac'],
                education_level=row['education_level'],
                preferences=preferences,
                tags=set(row['tags']),
                threshold=float(row['threshold'])
            )
            
            # Append the Profile object to the list
            profiles.append(profile)
        
        return profiles
    
    def random_profile_chooser(self, user, input_parquet_path: str, n):
        # Read the Parquet file into a DataFrame
        table = pq.read_table(input_parquet_path)
        df = table.to_pandas()
                
        # Ensure that there are enough profiles for the specified city
        if len(df) < n:
            print(f"There are only {len(df)} profiles available for {input_parquet_path}.")
            return None
        
        
        # Randomly select n profiles from the filtered DataFrame
        selected_profiles = random.sample(df.index.tolist(), n)
        
        # Retrieve the selected profiles
        selected_data = df.loc[selected_profiles]
        
        profiles = []
        for _, row in selected_data.iterrows():
            preferences = json.loads(row['preferences'])
            profile = Profile(
                id=str(row['id']),
                age=int(row['age']),
                religion=row['religion'],
                location=row['location'],
                zodiac=row['zodiac'],
                education_level=row['education_level'],
                preferences=preferences,
                tags=set(row['tags']),
                threshold=float(row['threshold'])
            )
            
            # Ensure the user profile is not included in the retrieved profiles
            if user and profile.id != user.id:
                profiles.append(profile)
            elif not user:
                profiles.append(profile)
        
        return profiles  
    
    # def parquet_by_location(self, input_parquet_path, output_parquet_path, city):
    #     # Read the original Parquet file into a DataFrame
    #     original_table = pq.read_table(input_parquet_path)
    #     original_df = original_table.to_pandas()
        
    #     # Filter profiles by the specified city
    #     city_profiles = original_df[original_df['location'] == city]
        
    #     # Write the filtered DataFrame to a new Parquet file
    #     city_profiles.to_parquet(output_parquet_path, index=False)
            
    def parquet_by_location(self, input_parquet_path, output_parquet_path, city, num_profiles=None, exclude_ids=None):
        # Read the original Parquet file into a DataFrame
        original_table = pq.read_table(input_parquet_path)
        original_df = original_table.to_pandas()
        
        # Filter profiles by the specified city
        city_profiles = original_df[original_df['location'] == city]
        
        # Exclude the specified IDs if provided
        if exclude_ids:
            for exclude_id in exclude_ids:
                if isinstance(exclude_id, str):
                    city_profiles = city_profiles[city_profiles['id'] != exclude_id]
        
        # Limit the number of profiles if specified
        if num_profiles is not None:
            city_profiles = city_profiles.head(num_profiles)
        
        # Write the filtered DataFrame to a new Parquet file
        city_profiles.to_parquet(output_parquet_path, index=False)

        

#Update parquets from each city from new profiles_parquet
# ret = Retriever()
# ret.parquet_by_location("new_york_profiles.parquet", "new_york_profiles1000.parquet", "New York", 1000, ["b981f4d1-b649-4abb-b333-5d7dd69e8310", "2e6a8e21-6120-467e-8e83-46fb03400682", "3b355141-1488-4cbf-a4d0-70a706d1eb10"])
# ret.parquet_by_location("houston_profiles.parquet", "houston_profiles.parquet1000", "Houston", 1000)
# ret.parquet_by_location("boston_profiles.parquet", "boston_profiles.parquet1000", "Boston",1000)
# ret.parquet_by_location("chi_profiles.parquet", "chi_profiles.parquet1000", "Chicago",1000)
# ret.parquet_by_location("la_profiles.parquet", "la_profiles.parquet1000", "Los Angeles",1000)
# ret.parquet_by_location("philly_profiles.parquet", "philly_profiles.parquet1000", "Philadelphia",1000)
# ret.parquet_by_location("sf_profiles.parquet", "sf_profiles.parquet1000", "San Francisco",1000)

# print("done")

# ret.parquet_by_location("new_york_profiles.parquet", "new_york_profiles10000.parquet", "New York", 10000, ["b981f4d1-b649-4abb-b333-5d7dd69e8310", "2e6a8e21-6120-467e-8e83-46fb03400682", "3b355141-1488-4cbf-a4d0-70a706d1eb10"])
# ret.parquet_by_location("houston_profiles.parquet", "houston_profiles.parquet10000", "Houston", 10000)
# ret.parquet_by_location("boston_profiles.parquet", "boston_profiles.parquet10000", "Boston",10000)
# ret.parquet_by_location("chi_profiles.parquet", "chi_profiles.parquet10000", "Chicago",1000)
# ret.parquet_by_location("la_profiles.parquet", "la_profiles.parquet10000", "Los Angeles",10000)
# ret.parquet_by_location("philly_profiles.parquet", "philly_profiles.parquet10000", "Philadelphia",10000)
# ret.parquet_by_location("sf_profiles.parquet", "sf_profiles.parquet10000", "San Francisco",10000)
# print("done2")
#get lengths of each file
# df = pd.read_parquet("houston_profiles.parquet")
# print(len(df))
# df = pd.read_parquet("new_york_profiles.parquet")
# print(len(df))
# df = pd.read_parquet("la_profiles.parquet")
# print(len(df))
# df = pd.read_parquet("philly_profiles.parquet")
# print(len(df))
# df = pd.read_parquet("sf_profiles.parquet")
# print(len(df))
# df = pd.read_parquet("boston_profiles.parquet")
# print(len(df))
# df = pd.read_parquet("chi_profiles.parquet")
# print(len(df))
    
 