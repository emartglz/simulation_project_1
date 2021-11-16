from macros import (
    LARGE_ARRIVE_PROBABILITY,
    MEDIUM_ARRIVE_PROBABILITY,
    SMALL_ARRIVE_PROBABILITY,
    TIME_TO_ARRIVE,
)
from ship import ShipTypes
import rng
from random import choices

arrival_probability = {
    ShipTypes.small: SMALL_ARRIVE_PROBABILITY,
    ShipTypes.medium: MEDIUM_ARRIVE_PROBABILITY,
    ShipTypes.large: LARGE_ARRIVE_PROBABILITY,
}


def generate_arrive():

    arrive_time = rng.exponential(1 / TIME_TO_ARRIVE)

    ship_type = choices(
        [k for k in arrival_probability.keys()],
        [v for v in arrival_probability.values()],
    )

    return (arrive_time, ship_type[0])
