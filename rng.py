import random


def rng_range(val):
    return random.randint(-val, val)


if __name__ == "__main__":
    print(rng_range(10))
