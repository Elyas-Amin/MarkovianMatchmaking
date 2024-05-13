import matplotlib.pyplot as plt

class QValuesVisualizer:
    def __init__(self):
        self.q_values = []

    def update_q_values(self, q_values):
        self.q_values.append(q_values)

    def plot_q_values(self):
        plt.figure()
        for i in range(len(self.q_values[0])):
            plt.plot([q_values[i] for q_values in self.q_values], label=f'Action {i}')
        plt.xlabel('Episode')
        plt.ylabel('Q-value')
        plt.title('Q-values for State')
        plt.legend()
        plt.show()