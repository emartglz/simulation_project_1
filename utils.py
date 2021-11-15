from functools import reduce
from macros import INF


def min_of_list(list):
    return reduce(lambda a, b: min(a, b), list)


def get_position_of_min(list):
    min_pos = 0
    min_n = INF
    for i in range(len(list)):
        if list[i] < min_n:
            min_n = list[i]
            min_pos = i
    return min_pos


def is_full_none(list):
    for i in range(len(list)):
        if list[i] is not None:
            return False
    return True


def get_first_none(list):
    for i in range(len(list)):
        if list[i] is None:
            return i
    return None


def get_first_none_tuple(list, side):
    for i in range(len(list)):
        if list[i][0] is None and list[i][2] == side:
            return i
    return None
