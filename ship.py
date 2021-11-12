from enum import Enum
from numpy.lib.function_base import median
from numpy.random import default_rng


class ShipTypes(Enum):
    small = "small"
    medium = "medium"
    large = "large"


times_for_load = {
    ShipTypes.small: (9, 1),
    ShipTypes.medium: (12, 2),
    ShipTypes.large: (18, 3),
}


def get_load_time(type):
    rng = default_rng()
    return rng.normal(times_for_load[type][0], times_for_load[type][1])
