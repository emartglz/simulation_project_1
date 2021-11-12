from numpy.random import default_rng
from enum import Enum


class TrailerSide(Enum):
    port = "port"
    pier = "pier"


def get_move_to_pier_time():
    rng = default_rng()
    return rng.exponential(1 / 2)


def get_move_to_port_time():
    rng = default_rng()
    return rng.exponential(1)


def get_swap_time():
    rng = default_rng()
    return rng.exponential(4)
