import random
from .SumTree import *


class Memory:
    def __init__(self, capacity, epsilon=1.0, alpha=0.5):
        self.tree = SumTree(capacity)
        self.epsilon = epsilon
        self.alpha = alpha

    def add(self, error, sample):
        p = self._get_priority(error)
        self.tree.add(p, sample)

    def sample(self, n):
        batch = []
        segment = self.tree.total() / n

        for i in range(n):
            a = segment * i
            b = segment * (i + 1)

            s = random.uniform(a, b)
            (idx, p, data) = self.tree.get(s)
            batch.append((idx, data))

        return batch

    def update(self, idx, error):
        p = self._get_priority(error)
        self.tree.update(idx, p)

    def _get_priority(self, error):
        return (error + self.epsilon) ** self.alpha