import numpy as np
import keras
from simulator import Simulator
import random
from visualizer import QValuesVisualizer
import matplotlib.pyplot as plt

import prof_char as p_char

from generator import generate_profile

class DQNAgent:
    def __init__(self, max_memory_size=1000):
        self.state_size = 30 # 30 features encoded in state
        self.action_size = 2 # Agent can suggest or not suggest a profile
        self.memory = []
        self.max_memory_size = max_memory_size
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self._build_model()
        self.losses = []


    def _build_model(self):
        input_layer = keras.layers.Input(shape=(self.state_size,))
        model = keras.Sequential()
        model.add(input_layer)
        model.add(keras.layers.Dense(24, activation='relu'))
        model.add(keras.layers.Dense(24, activation='relu'))
        model.add(keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=0.001))
        return model
    
    def encode_state(self, user, match):
        # Encode user's age, education level, religion, zodiac sign
        user_state = np.array([
            user.age,
            p_char.e.index(user.education_level),
            p_char.r.index(user.religion),
            p_char.z.index(user.zodiac)
        ])

        # Encode match profile's characteristics
        match_state = np.zeros(len(p_char.r) + len(p_char.l) + len(p_char.z) + 1)
        match_state[p_char.r.index(match.religion)] = 1 # religion
        match_state[len(p_char.r) + p_char.l.index(match.location)] = 1 # location
        match_state[len(p_char.r) + len(p_char.l) + p_char.z.index(match.zodiac)] = 1 # zodiac
        match_state[len(match_state) - 1] = match.age # age

        return np.concatenate((user_state, match_state))

    def remember(self, state, action, reward, next_state):
        self.memory.append((state, action, reward, next_state))
        if len(self.memory) > self.max_memory_size:
            self.memory.pop(0)  # Remove the oldest experience

    def act(self, state):
        if np.random.rand() <= self.epsilon:
            # Randomly select an action: 0 for not suggesting, 1 for suggesting
            return random.randint(0, 1)
        else:
            # Use the model to predict the action
            state = np.expand_dims(state, axis=0)
            act_values = self.model.predict(state, batch_size=None)
            return np.argmax(act_values[0])

    # Inside the replay method
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        # Sample a minibatch of experiences from memory
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state in minibatch:

            # Calculate the target value for the Q-network
            next_state = np.expand_dims(next_state, axis=0)
            reward = (reward + self.gamma * np.amax(self.model.predict(next_state, batch_size=None)[0]))
            
            state = np.expand_dims(state, axis=0)
            q_value = self.model.predict(state, batch_size=None) # Get the current Q-values for the state
            q_value[0][action] = reward # Update the Q-value for the selected action
            history = self.model.fit(state, q_value, epochs=1, verbose=0)
            self.losses.append(history.history['loss'][0])

            # self.model.fit(state, target_f, epochs=1, verbose=0) # Train the Q-network using the updated Q-value

        # Update epsilon (exploration rate) using epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def unsupervised_learning(self, user, profiles, simulator):
        suggested = 0
        accepts = 0
        while profiles:
            # 20 profiles per episode
            for _ in range(20):
                if len(profiles) == 0:
                    break

                # Select an action using the agent's policy
                match = profiles.pop()
                state = self.encode_state(user, match)
                action = self.act(state)
                if action == 1:
                    suggested += 1

                    # Get user's response
                    response = simulator.decision(user, match)
                    reward = 100 if response else -5
                    if response:
                        accepts += 1

                    # Encode the new state based on the user's response
                    next_state = self.encode_state(user, match)

                else:
                    # If no profile is suggested, the state remains the same
                    next_state = state
                    reward = 0

                # Remember the experience
                agent.remember(state, action, reward, next_state)

                # Set the current state to the new state
                state = next_state

            # Update the agent at the end of each episode
            agent.replay(30)

        return accepts, suggested
    
    def save_model(self, filename):
        self.model.save(filename)


# Initialize the environment and DRL agent
agent = DQNAgent()
simulator = Simulator()

# # Fetch user and profiles from the database
# retriever = Retriever()
# training_set = []
# for _ in range(1):
#     training_set.append(retriever.random_profiles(1000))


user = generate_profile(p_char.r, p_char.l, p_char.z, p_char.e, p_char.t)
profiles = set()

for _ in range(1000):
    profiles.add(generate_profile(p_char.r, p_char.l, p_char.z, p_char.e, p_char.t))

accepts, suggested = agent.unsupervised_learning(user, profiles, simulator)

print(user)
print("accepts ", accepts)
print("suggested ", suggested)

plt.plot(agent.losses)
plt.xlabel('Step')
plt.ylabel('Loss')
plt.title('Learning Loss')
plt.show()