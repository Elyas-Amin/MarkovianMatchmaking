from generator import generate_profile
from simulator import Simulator
from csp import CSP
from drl import DQNAgent
import matplotlib.pyplot as plt

user = generate_profile()
profiles = []

num = 1000
for _ in range(num):
    profiles.append(generate_profile())

csp = CSP()

user_matches = {
    "age_range": [],
    "zodiac_pref": [],
    "education_pref": [],
    "tag_similarity" : []
}

matches = csp.match_profiles(user, profiles.copy(), user_matches)
match_set = set()
for var, profs in matches.items():
    for p in profs:
        if p not in match_set:
            match_set.add(p)


# Initialize the simulator
simulation = Simulator()
agent = DQNAgent()

# Simulate the user's decisions
rand_accepts, rand_rejects, rand_rt = simulation.simulation(user, profiles.copy())
csp_accepts, csp_rejects, csp_rt = simulation.simulation(user, list(match_set))
drl_accepts, drl_suggested, drl_rt = agent.unsupervised_learning(user, profiles.copy(), simulation)

print(user)
print(len(rand_accepts), num, sum(rand_rt)/len(rand_rt) if len(rand_rt) > 0 else None)
print(len((csp_accepts)), len(match_set) if len(match_set) > 0 else 0, sum(csp_rt)/len(csp_rt) if len(csp_rt) > 0 else None)
print(len(drl_accepts), len(drl_suggested), sum(drl_rt)/len(drl_rt) if len(drl_rt) > 0 else None)

agent.visualize_q_values(agent.q_value_frames, 'q_value_visualization.gif')
agent.save_loss_plot(agent.losses, 'learning_loss_plot.png')