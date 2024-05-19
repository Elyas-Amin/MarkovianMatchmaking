from generator import generate_profile
from simulator import Simulator
from csp import CSP
from drl import DQNAgent
import matplotlib.pyplot as plt
from retriever import Retriever
import time
import timeit

START_TIME = 0
STOP_TIME = 0

##################INTIALIZATION#############
csp = CSP()
retriever = Retriever()
simulation = Simulator()
agent = DQNAgent()

#####################USER_AND_DATASET_GENERATION############
num = 100
city = "New York"
input_parquet_path = "new_york_profiles.parquet"

#generate the user
user = retriever.retrieve_by_location(city, 1)[0]

#get list of profiles based on city and num
profiles = retriever.random_profile_chooser(user, input_parquet_path, num)

#make sure user not in profiles
while user in profiles:
    user = retriever.retrieve_by_location(city, 1)[0]


####################CSP_SETUP##########################
# user_matches = {
#     "age_range": [],
#     "zodiac_pref": [],
#     "education_pref": [],
#     "tag_similarity" : []}

#match with CSP
# matches = csp.match_profiles(user, profiles.copy(), user_matches)
# match_set = set() #storing the matches

# #collect CSP matches
# for var, profs in matches.items():
#     for p in profs:
#         if p not in match_set:
#             match_set.add(p)

# print("match set length:", len(match_set))


#############RUNNING_SIMULATION###################
# rand_accepts, rand_rejects, rand_rt = simulation.simulation(user, profiles.copy())
# print("random sim done")
# csp_accepts, csp_rejects, csp_rt = simulation.simulation(user, list(match_set))
# print("csp sim done")
START_TIME = timeit.default_timer()

drl_accepts, drl_suggested, drl_rt = agent.unsupervised_learning(user, profiles.copy(), simulation)
STOP_TIME = timeit.default_timer()
print(STOP_TIME-START_TIME)
# print(user)
# print("Accepts ", len(rand_accepts), "; Suggested ", num, "; Running Time ", sum(rand_rt)/len(rand_rt) if len(rand_rt) > 0 else None)
# print("Accepts ", len((csp_accepts)), "; Suggested ", len(match_set) if len(match_set) > 0 else 0, "; Running Time ", sum(csp_rt)/len(csp_rt) if len(csp_rt) > 0 else None)
print("Accepts ", len(drl_accepts), "; Suggested ", len(drl_suggested), "; Running Time ", sum(drl_rt)/len(drl_rt) if len(drl_rt) > 0 else None)

agent.visualize_q_values(agent.q_value_frames, 'q_value_visualization.gif')
agent.save_loss_plot(agent.losses, 'learning_loss_plot.png')