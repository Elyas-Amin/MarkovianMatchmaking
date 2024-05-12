class Profile:
    def __init__(self, id: int, age: int, religion: str, location: str, zodiac:str, education_level: str, preferences):
    def __init__(self, id: int, age: int, religion: str, location: str, zodiac:str, education_level: str, preferences):
        self.id = id
        self.age = age
        self.religion = religion
        self.location = location
        self.zodiac = zodiac
        self.education_level = education_level
        self.tags = set()
        self.preferences = preferences

    def compute_compatibility(self, match):
        # Calculate tag similarity
        tag_score = len(self.tags.intersection(match.tags))

        # Calculate age difference score
        age_diff = abs(self.age - match.age)
        age_score = 1 / (1 + age_diff)  # Scale to range [0, 1]

        # Calculate preferences compatibility
        pref_score = 0
        for key in self.preferences:
            if key in match.preferences:
                self_prefs = self.preferences[key]
                match_prefs = match.preferences[key]
                if isinstance(self_prefs, (list, set)) and isinstance(match_prefs, (list, set)):
                    common_prefs = set(self_prefs).intersection(match_prefs)
                    pref_score += len(common_prefs) / len(self_prefs) if len(self_prefs) > 0 else 0

        # Combine scores with weights
        compatibility_score = (tag_score + age_score + pref_score) / 3  # Adjust weights as needed

        return compatibility_score

    
    def __repr__(self):
        return f'\[{self.id}, {self.age}, {self.religion}, {self.location}, {self.zodiac}, {self.education_level}, {self.tags}, {self.preferences}\]'