import gym
import numpy as np
import jax
from gym.utils.seeding import np_random


def sigmoid(x):
    return (np.tanh(x) + 1) / 2


class DebugEnv(gym.Env):
    def __init__(
        self, levels: int, std: float, dim: int = None,
    ):
        self.std = std
        self.random, _ = np_random(0)
        levels += 1
        self.embeddings = np.eye(levels)
        self.acceptable = self.random.random(levels)
        self.iterator = None
        self.observation_space = gym.spaces.Box(
            low=np.zeros(levels), high=np.ones(levels)
        )
        self.action_space = gym.spaces.Box(low=np.zeros(1), high=np.ones(1))
        self._max_episode_steps = 2
        self._render = None

    def seed(self, seed=None):
        self.random, _ = np_random(seed)

    def generator(self):
        t = False
        r = 0
        action = yield self.embeddings[0], r, False, {}
        for embedding, acceptable in zip(self.embeddings[1:-1], self.acceptable):

            def render():
                print(acceptable)

            self._render = render
            action = yield embedding, r, t, {}
            # normal = self.random.normal(scale=self.std)
            r = -abs(action - acceptable).item()
            # t = abs(normal) < diff
        r = -abs(action - self.acceptable[-1]).item()
        yield self.embeddings[-1], r, True, {}

    def step(self, action):
        return self.iterator.send(action)

    def reset(self):
        self.iterator = self.generator()
        s, _, _, _ = next(self.iterator)
        return s

    def render(self, mode="human"):
        self._render()


def play():
    env = DebugEnv(levels=100, dim=100, std=100)
    _ = env.reset()
    while True:
        env.render()
        action = float(input("go"))
        _, r, t, i = env.step(action)
        print("reward:", r)
        print("done:", t)


if __name__ == "__main__":
    play()
