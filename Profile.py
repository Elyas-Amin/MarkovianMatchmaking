class Profile:
    def __init__(self, name: str, age: int, religion: str, location: str, zodiac:str, education_level: str):
        self.name = name
        self.age = age
        self.religion = religion
        self.location = location
        self.zodiac = zodiac
        self.education__level = education_level
        self.tags = {}
        self.comptability = {}
        
    def compute_compatabilty(self, match: Profile):
        tags_score = len(self.tags.union(match.tags))
        score = tags_score
        return score
        