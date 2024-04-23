import numpy as np
from Profile import Profile

r = ['Buddhist', 'Zoroastrian', 'Christian', 'Jewish', 'Muslim', 'Hindu']
l = ['San Francisco', 'New York', 'Los Angeles', 'Chicago', 'Boston', 'Houston',
             'Philadelphia']
z = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius','Pisces']
e = ['high school', 'undergraduate', 'graduate']
t = ['tennis', 'swimming', 'art', 'museum', 'cooking', 'romantic']



def generate_profile(religions, locations, zodiac_signs, education_levels, tags):
    p = Profile

    # use discrete uniform distribution to generate profile characteristics
    p.age = np.random.randint(18, 100)
    p.religion = religions[np.random.randint(len(religions))]
    p.location = locations[np.random.randint(len(locations))]
    p.zodiac = zodiac_signs[np.random.randint(len(zodiac_signs))]
    p.education_level = education_levels[np.random.randint(len(education_levels))]

    # random number of tags chosen uniformly from list
    for i in range(np.random.randint(len(tags))):
        p.tags.add(tags[np.random.randint(len(tags))])
    
    return p


def generate_database(size):
    database = {}
    for x in range(size):
        database.add(generate_profile(r, l, z, e, t))
    
    return database

if __name__ == '__main__':
    
    profiles = generate_database(100)

    # Setup output file
    out_filename = 'generated_profiles.txt'
    outfile = open(out_filename, "w")


    # Write board to file
    for profile in profiles:
        outfile.write()
        outfile.write(',')