import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.layers import Input
from Profile import Profile
from simulator import Simulator
import random
import sqlite3
import json
import matplotlib.pyplot as plt

class DQNAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self._build_model()
        self.q_values = []

    def _build_model(self):
        input_layer = Input(shape=(self.state_size,))
        model = tf.keras.Sequential()
        model.add(input_layer)
        model.add(Dense(24, activation='relu'))
        model.add(Dense(24, activation='relu'))
        model.add(Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=Adam(learning_rate=0.001))
        return model

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.action_size)
        act_values = self.model.predict(state)
        return np.argmax(act_values[0])

    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return
        
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, done in minibatch:
            target = reward
            if not done:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            target_f = self.model.predict(state)
            target_f[0][action] = target
            self.model.fit(state, target_f, epochs=1, verbose=0)
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def update_q_values(self, state):
        q_values = self.model.predict(state)[0]
        self.q_values.append(q_values)

# Initialize the environment and DRL agent
state_size = 2  # Assuming state includes user's age and education level
action_size = 3  # Assuming three possible profiles to suggest
agent = DQNAgent(state_size, action_size)
simulator = Simulator()

# Fetch user and profiles from the database
# Connect to the SQLite database
conn = sqlite3.connect('profiles.db')
c = conn.cursor()

# Get the list of all profile IDs
c.execute("SELECT id FROM profiles")
all_profile_ids = [row[0] for row in c.fetchall()]

# Select a random user profile ID
user_profile_id = random.choice(all_profile_ids)

# Select 1000 random profiles excluding the user profile
other_profiles = random.sample([id for id in all_profile_ids if id != user_profile_id], 1000)

# Fetch the user profile
c.execute("SELECT * FROM profiles WHERE id=?", (user_profile_id,))
user_row = c.fetchone()

# Parse the preferences column from JSON to dictionary
preferences = json.loads(user_row[6])  # Assuming preferences is the 7th column (index 6)

# Create a Profile instance for the user
user = Profile(user_row[0], user_row[1], user_row[2], user_row[3], user_row[4], user_row[5], preferences)

# Fetch the other profiles and convert them to Profile instances
other_profiles_instances = []
for profile_id in other_profiles:
    c.execute("SELECT * FROM profiles WHERE id=?", (profile_id,))
    profile_row = c.fetchone()
    preferences = json.loads(profile_row[6])
    profile_instance = Profile(profile_row[0], profile_row[1], profile_row[2], profile_row[3], profile_row[4], profile_row[5], preferences)
    other_profiles_instances.append(profile_instance)

# Close the connection
conn.close()

# Simulation loop
plt.figure()
for episode in range(1000):
    for _ in range(10):  # Assuming 10 actions per episode
        # Select a random profile to suggest
        suggested_profile = random.choice(other_profiles_instances)
        # Simulate user's response
        user_state = np.array([[user.age, 1 if user.education_level == "Master's" else 0]])  # Example state encoding
        action = agent.act(user_state)
        response = simulator.decision(user, suggested_profile)
        reward = 1 if response == "accept" else -1
        # Remember the experience
        agent.remember(user_state, action, reward, user_state, False)
    # Update the agent at the end of each episode
    agent.replay(32)
    # Update Q-values for a specific state
    agent.update_q_values(user_state)
    
    # Plot the Q-values for the specific state
    plt.clf()  # Clear the previous plot
    for i in range(agent.action_size):
        plt.plot([q_values[i] for q_values in agent.q_values], label=f'Action {i}')
    plt.xlabel('Episode')
    plt.ylabel('Q-value')
    plt.title('Q-values for State')
    plt.legend()
    plt.pause(0.01)  # Pause to update the plot
plt.show()


