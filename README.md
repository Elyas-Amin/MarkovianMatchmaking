# MarkovianMatchmaking

MarkovianMatchmaking is an innovative project aimed at developing a sophisticated matchmaking algorithm for online dating platforms. Our objective is to enhance users' dating experiences by learning their preferences and presenting them with the most compatible profiles. We have designed two distinct algorithms leveraging Markov Decision Processes (MDP), Deep Reinforcement Learning (DRL), and Constraint Satisfaction Problems (CSP). These algorithms simulate user decisions to accept or reject suggested profiles, with the DRL approach dynamically learning user preferences over time and the CSP approach optimizing the search space to find the best possible matches. Our system generates a synthetic dataset of profiles using diverse interest tags and demographic information to evaluate the algorithms' performance. By comparing expected running times and analyzing various metrics, we aim to maximize user satisfaction and provide a robust solution for effective matchmaking.

## Usage

To run the matchmaking simulation, you can use the provided driver file `driver.py`. This script initializes the necessary components, retrieves user and profile data, and runs the simulations using CSP and a random selection method.

### Running the Driver File

1. Ensure all required packages are installed:
    ```bash
    pip install numpy pandas pyarrow keras tensorflow seaborn imageio matplotlib
    ```

2. Execute the driver script:
    ```bash
    python driver.py
    ```

### Modifiable Parameters

The `driver.py` script includes several parameters that can be adjusted to customize the simulation:

- **City** (`city`): Specifies the city from which profiles should be retrieved. Default is "New York".
    ```python
    city = "New York"
    ```

- **Input Parquet Path** (`input_parquet_path`): Path to the parquet file containing the profile data. Parquet files contain a specified number of profiles. Default is "new_york_profiles.parquet".
    ```python
    input_parquet_path = "new_york_profiles.parquet"
    ```

- **Retriever Functions**: The single user or the pool of profiles can be modified by choosing which retriever function from retriever.py is used.

These parameters can be modified directly in the `driver.py` script to tailor the simulation to different datasets or requirements.

### Example
Here is a simple example to illustrate how you can modify the parameters:
```python
# Example: Modify the number of profiles to 50,000 and the city to "San Francisco"
city = "San Francisco"
input_parquet_path = "san_francisco_profiles.parquet"

## Packages Required
- numpy
- pandas
- pyarrow
- keras
- tensorflow
- seaborn
- imageio

### Installation
To install the required packages, you can use pip:
```bash
pip install numpy pandas pyarrow keras tensorflow seaborn imageio
```

## Challenges and Future Work
### Challenges
- **Implementation Constraints**: We were unable to implement constraint acquisition in the CSP model due to time limitations.
- **Software Dependencies**: Encountered difficulties with software dependencies while implementing the DQN agent, which relies on a complex set of libraries and tools.
- **Virtual Environments**: Managing virtual environments was problematic, as they would often stop working, necessitating the creation of copies of files to continue work.
- **Time Constraints**: Limited time prevented us from fine-tuning the DRL model and fully optimizing the algorithms.
- **Computational Power**: Insufficient computational power restricted our ability to run tests on much larger input sizes, which would have provided a more thorough evaluation of the algorithms' scalability.
- **Consultation and Method Adjustments**: Spent considerable time consulting a professor about the Markov process simulation, leading to shifts in evaluation methods based on her recommendations to ensure statistical soundness.
- **Experimental Values**: A small number of experimental values made it difficult to draw definitive conclusions.
- **Variance Reduction**: The lack of variance reduction techniques complicated the analysis, making it challenging to achieve more precise results.

### Future Work
- **Refining Metrics**: Adding and refining metrics for personality traits such as visual attractiveness, socioeconomic status, and peer groups.
- **User Actions**: Algorithms can take into account actions from similar users and update policies or constraints accordingly.
- **Reciprocal Interests**: Incorporating reciprocal interests and interactions on the platform to update the algorithms dynamically.
- **Improving the Simulator**: Enhancing the simulator to better mimic user behavior by considering more factors in decision making and introducing more probabilities based on historical interactions.
- **Hybrid Model**: Designing a hybrid system that combines the strengths of CSP and DRL to optimize matchmaking more effectively.