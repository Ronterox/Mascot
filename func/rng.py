import random
import time

random.seed(time.time())

def rng_range(start, end=None):
    return random.randint(-start, start) if end is None else random.randint(start, end)

def rng_choice(sequence):
    return random.choice(sequence)

if __name__ == "__main__":
    print(rng_range(10))
