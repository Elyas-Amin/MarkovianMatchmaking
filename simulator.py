import numpy as np
from profile import Profile

class Simulator:
    def __init__(self):
        self.acceptance_history = []

    def decision(self, user: Profile, profile: Profile):
        '''Decisions are made based on compatibility score following a sigmoid function'''

        compatibility_score = user.compute_compatibility(profile)
        
        # Sigmoid scaling factor and shifting constant
        a = 1  # shape of the sigmoid
        b = user.threshold # x-axis shift adjsut the sigmoid so the center is tat hte htreshold

        # Calculate acceptance probability, function for sigmoid function
        acceptance_score= 1 / (1 + np.exp(-a * compatibility_score + b))

        # Make decision based on acceptance score + value for variability when vlaue is close to the threshold
        return (acceptance_score + np.random.normal(-0.01, 0.01)) >= 0.5

    def simulation(self, user: Profile, profiles):
        '''Tick-based simulation of user deciding on each profile from set of profiles'''
        accepts = set()
        rejects = set()
        running_times = []
        counter = 0

        while profiles:
            profile = profiles.pop()
            if self.decision(user, profile):
                accepts.add(profile)
                running_times.append(counter)
                counter = 0
            else:
                rejects.add(profile)
                counter += 1

        return accepts, rejects, running_times
