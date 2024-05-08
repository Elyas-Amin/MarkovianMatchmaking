import numpy as np
import stat
from profile import Profile

def decision(user: Profile, profile: Profile):
    decision = 0

    np.stat.normal(len())

    return decision

def tick_simulation(user: Profile, profiles):
    '''Tick-based simulation of user deciding on each profile from set of profiles'''
    accepts = set()
    rejects = set()
    count = len(profiles)


    while profiles:
        profile = profiles.pop()
        if decision(user, profile):
            accepts.add(profile)
        else:
            rejects.add(profile)

    return accepts, rejects

if __name__ == '__main__':

    # user to be making decision
    #user = 
    #profiles = 

    # cluster of profiles to be decided on
    #profiles = csp(user, profiles)

    #print(tick_simulation(user, profiles))

