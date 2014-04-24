import random


class Random(object):

    def __init__(self, max_size=5):
        random.seed(0)
        self.max_size = max_size

    def next(self):
        return int(random.random() * self.max_size)
