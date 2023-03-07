import random


def rng_range(start, end=None):
    return random.randint(-start, start) if end is None else random.randint(start, end)

if __name__ == "__main__":
    print(rng_range(10))
