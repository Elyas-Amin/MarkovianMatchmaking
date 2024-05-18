import numpy as np
import json

class Profile:
    def __init__(self, id: int, age: int, religion: str, location: str, zodiac:str, education_level: str, tags: set, preferences, threshold: float):
        self.id = id
        self.age = age
        self.religion = religion
        self.location = location
        self.zodiac = zodiac
        self.education_level = education_level
        self.tags = tags
        self.preferences = preferences
        self.threshold = threshold
        
    def tag_overlap(self, potential_match):
        tag_score = len(self.tags.intersection(potential_match.tags))
        self.preferences["tag_similarity"] = tag_score

    def compute_compatibility(self, match):
        # Calculate tag similarity
        if len(self.tags.intersection(match.tags)) == 0:
            tag_score = 0
        else:
            tag_score = np.log2(len(self.tags.intersection(match.tags))+ 1) / 4.0

        # Calculate age difference score
        age_score = 1 / (1 + abs(self.age - match.age))

        # Calculate preferences compatibility.
        #Can we jsutify weights adn calues with a survey/research study?
        pref_score = 0
        if match.zodiac in self.preferences["zodiac_pref"]:
            pref_score += 1
        if match.education_level in self.preferences["education_pref"]:
            pref_score += 2
        if self.preferences["religion_pref"] == "open to all":
            pref_score += 1
        else:
            if match.religion in self.preferences["religion_pref"]:
                pref_score += 1
        pref_score /= 3

        # Combine scores with weights
        w1 = 0.4
        w2 = 0.2
        w3 = 0.4
        compatibility_score = w1 * tag_score + w2 * age_score + w3 * pref_score  # Adjust weights as needed

        return compatibility_score
    
    def to_dict(self):
        # Convert preferences dictionary to JSON string
        temp = list(self.preferences["zodiac_pref"])
        temp2 = self.preferences
        temp2["zodiac_pref"] = temp
        preferences_json = json.dumps(self.preferences)
        return {
            'id': self.id,
            'age': self.age,
            'religion': self.religion,
            'location': self.location,
            'zodiac': self.zodiac,
            'education_level': self.education_level,
            'preferences': preferences_json,
            'tags': list(self.tags),
            'threshold': self.threshold
        }
    
    def __repr__(self):
        return f'\[{self.id}, {self.age}, {self.religion}, {self.location}, {self.zodiac}, {self.education_level}, {self.tags}, {self.preferences}, {self.threshold}\]'
