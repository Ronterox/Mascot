import random


def rng_quote():
    return random.choice(open('quotes.txt').readlines())


def rng_range(val):
    return random.randint(-val, val)


if __name__ == "__main__":
    print(rng_quote())
    print(rng_range(10))
