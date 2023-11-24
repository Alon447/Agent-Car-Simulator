import gymnasium as gym
import numpy as np
from torch.nn import Sequential
from tensorflow.keras.layers import Dense


class AI_Env(gym.Env):
    def __init__(self):
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=0, high=1, shape=(2,), dtype=int)
    def reset(self, **kwargs):
        self.location = 0
        self._target_location = 5
        observation = self.location, self._target_location
        info={'target_location': self._target_location}
        return observation, info

    def step(self, action):
        self.location += action
        terminated = np.array_equal(self.location, self._target_location)
        reward = 1 if terminated else -1
        observation = self.location, self._target_location
        info={'target_location': self._target_location}
        return observation, reward, terminated, False, info

    def render(self):
        pass

if __name__ == "__main__":

    def build_model(states, actions):
        model = Sequential()
        # model.add(Dense(24, input_dim=states, activation='relu'))
        # model.add(Dense(24, activation='relu'))
        # model.add(Dense(actions, activation='linear'))
        return model

    env = AI_Env()
    build_model(env.observation_space.shape[0], env.action_space)
    observation = env.reset()
    terminated = False
    for epoch in range(3):
        action = env.action_space.sample()
        observation, reward, terminated,_, info = env.step(action)
        print(f'Epoch: {epoch}, Observation: {observation}, Reward: {reward}, Terminated: {terminated}, Info: {info}')