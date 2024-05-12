import numpy as np
from profile import Profile

class Simulator:

    def decision(self, user: Profile, profile: Profile):
        '''Decisions are made based on compatibility scorefollowing a sigmoid function'''
        compatibility_score = user.compute_compatibility(profile)
        
        # Define scaling factor and shifting constant
        a = 1  # shape of the sigmoid
        b = 0  # x-axis shift

        # Calculate acceptance probability
        acceptance_probability = 1 / (1 + np.exp(-a * compatibility_score + b))
        
        # Make decision based on acceptance probability
        decision = np.random.choice([0, 1], p=[1 - acceptance_probability, acceptance_probability])
        return decision

    def simulation(self, user: Profile, profiles):
        '''Tick-based simulation of user deciding on each profile from set of profiles'''
        accepts = set()
        rejects = set()

        while profiles:
            profile = profiles.pop()
            if self.decision(user, profile):
                accepts.add(profile)
            else:
                rejects.add(profile)

        return accepts, rejects
