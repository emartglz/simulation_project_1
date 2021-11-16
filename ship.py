from enum import Enum
import rng


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
    return rng.normal(times_for_load[type][0], times_for_load[type][1])
