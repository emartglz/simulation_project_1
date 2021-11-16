import math
from numpy.random import default_rng


def exponential(l):
    u = default_rng().uniform()
    return -1 / l * math.log(u)


def discret_uniform(n):
    u = default_rng().uniform()
    return 1 + int(u * n)


def normal(miu, o_pow2):
    u = default_rng().uniform()
    y = exponential(1)

    if u <= math.pow(math.e, (-1 * math.pow(y - 1, 2)) / 2):
        ud = discret_uniform(2)
        if ud == 1:
            y *= -1

        return y * math.sqrt(o_pow2) + miu

    return normal(miu, o_pow2)
