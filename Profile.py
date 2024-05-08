class Profile:
    def __init__(self, id: int, age: int, religion: str, location: str, zodiac:str, education_level: str):
        self.id = id
        self.age = age
        self.religion = religion
        self.location = location
        self.zodiac = zodiac
        self.education_level = education_level
        self.tags = set()
        self.compatabile_profiles = set()
        self.preferences = set() 
        
    def compute_compatibility(self, match): #normalize comptability between 0 and 1
        tags_score = len(set.intersection(self.tags, match.tags))
        return tags_score
    
    def __repr__(self):
        return f'\[{self.id}, {self.age}, {self.religion}, {self.location}, {self.zodiac}, {self.education_level}, {self.tags}\]'