import numpy as np
import keras
import random
import seaborn as sns
import imageio.v2 as imageio
import matplotlib.pyplot as plt
import os

import prof_char as p_char
from simulator import Simulator
from generator import generate_profile

class DQNAgent:
    def __init__(self, max_memory_size=10000):
        print("here")
        self.state_size = 30  # 30 features encoded in state
        self.action_size = 2  # Agent can suggest or not suggest a profile
        self.memory = []
        self.max_memory_size = max_memory_size
        self.gamma = 0.95  # Discount rate
        self.epsilon = 1.0  # Exploration rate
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.model = self._build_model()
        self.losses = []
        self.q_value_frames = []  # For storing Q-values for visualization


    def _build_model(self):
        ''' Build the Q-network model '''
        input_layer = keras.layers.Input(shape=(self.state_size,))
        model = keras.Sequential()
        model.add(input_layer)
        model.add(keras.layers.Dense(24, activation='relu'))
        model.add(keras.layers.Dense(24, activation='relu'))
        model.add(keras.layers.Dense(self.action_size, activation='linear'))
        model.compile(loss='mse', optimizer=keras.optimizers.Adam(learning_rate=0.001))
        return model
    
    def encode_state(self, user, match):
        ''' Encode the state from user and match profiles '''
        user_state = np.array([
            user.age,
            p_char.e.index(user.education_level),
            p_char.r.index(user.religion),
            p_char.z.index(user.zodiac)
        ])

        match_state = np.zeros(len(p_char.r) + len(p_char.l) + len(p_char.z) + 1)
        match_state[p_char.r.index(match.religion)] = 1
        match_state[len(p_char.r) + p_char.l.index(match.location)] = 1
        match_state[len(p_char.r) + len(p_char.l) + p_char.z.index(match.zodiac)] = 1
        match_state[len(match_state) - 1] = match.age

        return np.concatenate((user_state, match_state))


    def remember(self, state, action, reward, next_state):
        ''' Store the experience in memory '''
        self.memory.append((state, action, reward, next_state))
        if len(self.memory) > self.max_memory_size:
            self.memory.pop(0)  # Remove the oldest experience


    def act(self, state):
        ''' Choose an action based on the state '''
        if np.random.rand() <= self.epsilon:
            # Randomly select an action: 0 for not suggesting, 1 for suggesting
            return random.randint(0, 1)
        else:
            # Use the model to predict the action
            state = np.expand_dims(state, axis=0)
            act_values = self.model.predict(state, batch_size=None)
            return np.argmax(act_values[0])


    def replay(self, batch_size):
        ''' Replay experience for learning '''

        if len(self.memory) < batch_size:
            return

        # Sample a minibatch of experiences from memory
        minibatch = random.sample(self.memory, batch_size)

        for state, action, reward, next_state in minibatch:
            # Expand dims for model input
            next_state = np.expand_dims(next_state, axis=0)
            state = np.expand_dims(state, axis=0)

            # Calculate the target value for the Q-network
            target = reward + self.gamma * np.amax(self.model.predict(next_state, batch_size=1)[0])

            # Get the current Q-values for the state
            q_values = self.model.predict(state, batch_size=1)
            # Update the Q-value for the selected action
            q_values[0][action] = target

            # Train the model with the updated Q-values
            history = self.model.fit(state, q_values, epochs=1, verbose=0)
            self.losses.append(history.history['loss'][0])

        # Update epsilon (exploration rate) using epsilon decay
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def unsupervised_learning(self, user, profiles, simulator):
        ''' Train the agent using unsupervised learning '''

        suggested = set()
        accepts = set()
        running_times = []
        counter = 0

        while profiles:
            for _ in range(20):
                if len(profiles) == 0:
                    break
                
                # Agent decides action
                match = profiles.pop()
                state = self.encode_state(user, match)
                action = self.act(state)

                # Agent suggests profile to user
                if action == 1:
                    suggested.add(match)
                    counter += 1

                    response = simulator.decision(user, match)
                    reward = 10 if response else -5
                    
                    # User accepts the match profile
                    if response:
                        accepts.add(match)
                        running_times.append(counter)
                        counter = 0
                    next_state = self.encode_state(user, match)

                # Agent does not suggest profile to user
                else:
                    next_state = state
                    reward = 0

                # Remember experience
                self.remember(state, action, reward, next_state)
                state = next_state

            self.replay(30)
            
            # Capture Q-values at the specified interval
            sample_size = 50
            if len(self.memory) % sample_size == 0:
                sample_size = min(10, len(profiles))  # Adjust sample size to available profiles
                sample_states = [self.encode_state(user, profile) for profile in random.sample(profiles, sample_size)]
                q_values = self.get_q_values(sample_states)
                self.q_value_frames.append(q_values)
        return accepts, suggested, running_times
    
    def get_q_values(self, states):
        ''' Gets Q-values for sampled states '''

        q_values = []
        for state in states:
            state = np.expand_dims(state, axis=0)
            q_value = self.model.predict(state, batch_size=1)
            q_values.append(q_value[0])
        return np.array(q_values)
    
    def visualize_q_values(self, q_value_frames, filename_str):
        """ Visualize Q-values evolution over time as a GIF. """

        filenames = []
        for i, q_values in enumerate(q_value_frames):
            if q_values.size == 0:
                continue

            plt.figure(figsize=(10, 6))
            sns.heatmap(q_values, annot=True, fmt=".2f", cmap="viridis", xticklabels=["Not Suggest", "Suggest"], yticklabels=np.arange(q_values.shape[0]))
            plt.xlabel('Actions')
            plt.ylabel('States')
            plt.title(f'Q-values at Iteration {i * 50}')
            filename = f'q_values_{i}.png'
            plt.savefig(filename)
            filenames.append(filename)
            plt.close()

        with imageio.get_writer(filename_str, mode='I', fps = 5) as writer:
            for filename in filenames:
                image = imageio.imread(filename)
                writer.append_data(image)

        for filename in filenames:
            os.remove(filename)

    def save_loss_plot(self, losses, filename):
        ''' Save the learning loss plot as an image '''

        plt.plot(losses)
        plt.xlabel('Step')
        plt.ylabel('Loss')
        plt.title('Learning Loss')
        plt.savefig(filename)
        plt.close()
    
    def save_model(self, filename):
        ''' Save the model '''
        self.model.save(filename)

if __name__ == "__main__":
    # Initialize the environment and DRL agent
    agent = DQNAgent()
    simulator = Simulator()

    user = generate_profile()
    profiles = [generate_profile() for _ in range(1000)]

    accepts, suggested, running_times = agent.unsupervised_learning(user, profiles, simulator)

    print(user)
    print("accepts ", len(accepts))
    print("suggested ", len(suggested))

    # Visualize Q-values evolution and learning loss
    agent.visualize_q_values(agent.q_value_frames, 'q_value_visualization.gif')
    agent.save_loss_plot(agent.losses, 'learning_loss_plot.png')