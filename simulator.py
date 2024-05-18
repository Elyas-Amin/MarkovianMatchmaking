import numpy as np
from profile import Profile

class Simulator:
    def __init__(self):
        self.acceptance_history = []

    def decision(self, user: Profile, profile: Profile):
        '''Decisions are made based on compatibility score following a sigmoid function'''
        if user.location != profile.location:
            return False
        compatibility_score = user.compute_compatibility(profile)
        
        # Sigmoid scaling factor and shifting constant
        a = 1  # shape of the sigmoid
        b = user.threshold # x-axis shift

        # Calculate acceptance probability
        acceptance_score= 1 / (1 + np.exp(-a * compatibility_score + b))

        # Make decision based on acceptance score
        return (acceptance_score + np.random.uniform(-0.02, 0.02)) >= 0.5

    # def decision(self, user: Profile, profile: Profile):
    #     '''Decisions are made based on compatibility score following a sigmoid function'''
    #     compatibility_score = user.compute_compatibility(profile)
        
    #     # Define scaling factor and shifting constant
    #     a = 0.1  # Scaling factor
    #     b = 0    # x-axis shift

    #     # Calculate acceptance probability
    #     acceptance_probability = 1 / (1 + np.exp(-a * compatibility_score + b))
        
    #     # Make decision based on acceptance probability
    #     decision = np.random.choice([0, 1], p=[1 - acceptance_probability, acceptance_probability])

    #     if decision == 1:  # Accept the profile
    #         return True
    #     else:
    #         return False


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
