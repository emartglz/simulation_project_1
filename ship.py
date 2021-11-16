from enum import Enum
from macros import (
    LARGE_SHIP_LOAD_TIME_MU,
    LARGE_SHIP_LOAD_TIME_SIGMA2,
    MEDIUM_SHIP_LOAD_TIME_MU,
    MEDIUM_SHIP_LOAD_TIME_SIGMA2,
    SMALL_SHIP_LOAD_TIME_MU,
    SMALL_SHIP_LOAD_TIME_SIGMA2,
)
import rng


class ShipTypes(Enum):
    small = "small"
    medium = "medium"
    large = "large"


times_for_load = {
    ShipTypes.small: (SMALL_SHIP_LOAD_TIME_MU, SMALL_SHIP_LOAD_TIME_SIGMA2),
    ShipTypes.medium: (MEDIUM_SHIP_LOAD_TIME_MU, MEDIUM_SHIP_LOAD_TIME_SIGMA2),
    ShipTypes.large: (LARGE_SHIP_LOAD_TIME_MU, LARGE_SHIP_LOAD_TIME_SIGMA2),
}


def get_load_time(type):
    return rng.normal(times_for_load[type][0], times_for_load[type][1])
