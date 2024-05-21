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
    
    def parquet_by_location(self, input_parquet_path, output_parquet_path, city):
        # Read the original Parquet file into a DataFrame
        original_table = pq.read_table(input_parquet_path)
        original_df = original_table.to_pandas()
        
        # Filter profiles by the specified city
        city_profiles = original_df[original_df['location'] == city]
        
        # Write the filtered DataFrame to a new Parquet file
        city_profiles.to_parquet(output_parquet_path, index=False)
        

#Update parquets from each city from new profiles_parquet
# ret = Retriever()
# ret.parquet_by_location("profiles.parquet", "new_york_profiles.parquet", "New York")
# ret.parquet_by_location("profiles.parquet", "houston_profiles.parquet", "Houston")
# ret.parquet_by_location("profiles.parquet", "boston_profiles.parquet", "Boston")
# ret.parquet_by_location("profiles.parquet", "chi_profiles.parquet", "Chicago")
# ret.parquet_by_location("profiles.parquet", "la_profiles.parquet", "Los Angeles")
# ret.parquet_by_location("profiles.parquet", "philly_profiles.parquet", "Philadelphia")
# ret.parquet_by_location("profiles.parquet", "sf_profiles.parquet", "San Francisco")

#get lengths of each file
df = pd.read_parquet("houston_profiles.parquet")
print(len(df))
df = pd.read_parquet("new_york_profiles.parquet")
print(len(df))
df = pd.read_parquet("la_profiles.parquet")
print(len(df))
df = pd.read_parquet("philly_profiles.parquet")
print(len(df))
df = pd.read_parquet("sf_profiles.parquet")
print(len(df))
df = pd.read_parquet("boston_profiles.parquet")
print(len(df))
df = pd.read_parquet("chi_profiles.parquet")
print(len(df))
    
 