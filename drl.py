import numpy as np
import tensorflow as tf
import keras
from Profile import Profile
from simulator import Simulator
import random
from visualizer import QValuesVisualizer
from retriever import Retriever
import matplotlib.pyplot as plt
from keras.callbacks import Callback
from datetime import datetime

import prof_char as p_char

class DQNAgent:
    def __init__(self, state_size, action_size, max_memory_size=1000):
        self.state_size = state_size
        self.action_size = action_size
        self.memory = []
        self.max_memory_size = max_memory_size
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self._build_model()
        self.callbacks = [keras.callbacks.TensorBoard(log_dir='./logs')]
        log_dir = "logs/" + datetime.now().strftime("%Y%m%d-%H%M%S")
        self.tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1)
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

    def remember(self, state, action, reward, next_state, final):
        self.memory.append((state, action, reward, next_state, final))
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

        for state, action, reward, next_state, final in minibatch:

            # Calculate the target value for the Q-network
            target = reward # if experience was final state
            if not final:
                next_state = np.expand_dims(next_state, axis=0)
                target = (reward + self.gamma * np.amax(self.model.predict(next_state, batch_size=None)[0]))
            
            state = np.expand_dims(state, axis=0)
            target_f = self.model.predict(state, batch_size=None) # Get the current Q-values for the state
            target_f[0][action] = target # Update the Q-value for the selected action
            history = self.model.fit(state, target_f, epochs=1, verbose=0)
            self.losses.append(history.history['loss'][0])

            # self.model.fit(state, target_f, epochs=1, verbose=0) # Train the Q-network using the updated Q-value

        # Update epsilon (exploration rate) using epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay
    
    def save_model(self, filename):
        self.model.save(filename)


# Initialize the environment and DRL agent
state_size = 31
action_size = 2  # Assuming three possible profiles to suggest
agent = DQNAgent(state_size, action_size)
simulator = Simulator()
visualizer = QValuesVisualizer()

# Fetch user and profiles from the database
retriever = Retriever()
training_set = []
for _ in range(1):
    training_set.append(retriever.random_profiles(1000))

def encode_state(user_profile, suggested_profile):
    # Encode user's age, education level, religion, zodiac sign
    user_state = np.array([
        user_profile.age,
        p_char.e.index(user_profile.education_level),
        p_char.r.index(user_profile.religion),
        p_char.z.index(user_profile.zodiac)
    ])

    # Encode suggested profile's characteristics
    suggested_state = np.zeros(len(p_char.r) + len(p_char.l) + len(p_char.z) + 2)  #  2 extra slots for compatibility score and age
    suggested_state[p_char.r.index(suggested_profile.religion)] = 1
    suggested_state[len(p_char.r) + p_char.l.index(suggested_profile.location)] = 1
    suggested_state[len(p_char.r) + len(p_char.l) + p_char.z.index(suggested_profile.zodiac)] = 1

    # Compute compatibility score and discretize it
    compatibility_score = user_profile.compute_compatibility(suggested_profile)
    discretized_score = min(5, max(0, int(round(compatibility_score * 5))))
    suggested_state[len(suggested_state) - 1] = discretized_score
    suggested_state[len(suggested_state) - 2] = suggested_profile.age

    return np.concatenate((user_state, suggested_state))

for user, profiles in training_set:
    # Initialize the initial state to the user's state
    state = encode_state(user, profiles[0])  # Assuming the first profile is the initial suggestion

    # Simulation loop
    episode_length = 50  # Number of suggestions per episode
    for episode in range(100):
        suggested = 0
        accepts = 0
        print("Episode: ", episode)
        for _ in range(episode_length):

            # Select an action using the agent's policy
            action = agent.act(state)
            if action == 1:
                suggested += 1

                # Simulate user's response based on the selected action
                suggested_profile = profiles[action]
                response = simulator.decision(user, suggested_profile)
                reward = 10 if response else -5
                if response:
                    accepts += 1

                # Encode the new state based on the simulated interaction
                next_state = encode_state(user, suggested_profile)

            else:
                # If no profile is suggested, the state remains the same
                next_state = state
                reward = 0

            # Determine if this is the end of the episode
            final = _ == episode_length - 1  # Check if this is the last suggestion in the episode

            # Remember the experience
            agent.remember(state, action, reward, next_state, final)

            # Set the current state to the new state
            state = next_state

        if suggested != 0:
            print("accepts ", accepts/suggested)

        # Update the agent at the end of each episode
        agent.replay(32)

plt.plot(agent.losses)
plt.xlabel('Step')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.show()

# # Save the trained model
# agent.save_model("dqn_model.h5")