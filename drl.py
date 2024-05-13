import numpy as np
import tensorflow as tf
import keras
from Profile import Profile
from simulator import Simulator
import random
from visualizer import QValuesVisualizer
from retriever import Retriever
import pdb
from keras.callbacks import Callback


class DQNAgent:
    def __init__(self, state_size, action_size, max_memory_size=10000):
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
        state = np.expand_dims(state, axis = 0)
        print(np.array(state).shape)
        output = self.model.predict(np.array(state), batch_size = None)
        print("output ", output)
        pdb.set_trace()
        act_values = self.model.predict(state)
        print("act predict ", act_values)
        if np.random.rand() <= self.epsilon:
            # Randomly select an action: 0 for not suggesting, 1 for suggesting
            return random.randint(0, 1)
        else:
            # Use the model to predict the action
            act_values = self.model.predict(state)
            return np.argmax(act_values[0])

    # Inside the replay method
    def replay(self, batch_size):
        if len(self.memory) < batch_size:
            return

        # Sample a minibatch of experiences from memory
        minibatch = random.sample(self.memory, batch_size)

        for i, (state, action, reward, next_state, final) in enumerate(minibatch):
            print(f"Replaying experience {i}: state={state}, action={action}, reward={reward}, next_state={next_state}, final={final}")

            # Calculate the target value for the Q-network
            target = reward # if experience was final state
            if not final:
                target = (reward + self.gamma * np.amax(self.model.predict(next_state)[0]))
            
            target_f = self.model.predict(state) # Get the current Q-values for the state
            target_f[0][action] = target # Update the Q-value for the selected action

            self.model.fit(state, target_f, epochs=1, verbose=0) # Train the Q-network using the updated Q-value

        # Update epsilon (exploration rate) using epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay


# Initialize the environment and DRL agent
state_size = 31
action_size = 2  # Assuming three possible profiles to suggest
agent = DQNAgent(state_size, action_size)
simulator = Simulator()
visualizer = QValuesVisualizer()

# Fetch user and profiles from the database
retriever = Retriever()
user, profiles = retriever.random_profiles(1000)

# Trait mappings
r = ["Buddhist", "Zoroastrian", "Christian", "Jewish", "Muslim", "Hindu"]
l = ["San Francisco", "New York", "Los Angeles", "Chicago", "Boston", "Houston", "Philadelphia"]
z = ["aries", "taurus", "gemini", "cancer", "leo", "virgo", "libra", "scorpio", "sagittarius", "capricorn", "aquarius", "Pisces"]
e = ["high school", "undergraduate", "graduate"]
t = ["tennis", "swimming", "art", "museum", "cooking", "romantic"]
r_pref = ["open to all", "same"]

def encode_state(user_profile, suggested_profile):
    # Encode user's age, education level, religion, zodiac sign
    user_state = np.array([
        user_profile.age,
        e.index(user_profile.education_level),
        r.index(user_profile.religion),
        z.index(user_profile.zodiac)
    ])

    # Encode suggested profile's characteristics
    suggested_state = np.zeros(len(r) + len(l) + len(z) + 2)  #  2 extra slots for compatibility score and age
    suggested_state[r.index(suggested_profile.religion)] = 1
    suggested_state[len(r) + l.index(suggested_profile.location)] = 1
    suggested_state[len(r) + len(l) + z.index(suggested_profile.zodiac)] = 1

    # Compute compatibility score and discretize it
    compatibility_score = user_profile.compute_compatibility(suggested_profile)
    discretized_score = min(5, max(0, int(round(compatibility_score * 5))))
    suggested_state[len(suggested_state) - 1] = discretized_score
    suggested_state[len(suggested_state) - 2] = suggested_profile.age

    return np.concatenate((user_state, suggested_state))


# Initialize the initial state to the user's state
state = encode_state(user, profiles[0])  # Assuming the first profile is the initial suggestion

# Simulation loop
episode_length = 10  # Number of suggestions per episode
for episode in range(1000):
    print("Episode: ", episode)
    for _ in range(episode_length):
        # Select an action using the agent's policy
        action = agent.act(state)

        # Simulate user's response based on the selected action
        suggested_profile = profiles[action]
        response = simulator.decision(user, suggested_profile)
        reward = 10 if response == "accept" else -1

        # Encode the new state based on the simulated interaction
        next_state = encode_state(user, suggested_profile)

        # Determine if this is the end of the episode
        final = _ == episode_length - 1  # Check if this is the last suggestion in the episode

        # Remember the experience
        agent.remember(state, action, reward, next_state, final)

        # Set the current state to the new state
        state = next_state

    # Update the agent at the end of each episode
    print("replay")
    agent.replay(32)
    print("replay finished")

