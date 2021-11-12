from ship import ShipTypes
from numpy.random import default_rng
from random import choices

arrival_probability = {
    ShipTypes.small: 1 / 4,
    ShipTypes.medium: 1 / 4,
    ShipTypes.large: 1 / 2,
}


def generate_arrive():
    rng = default_rng()

    arrive_time = rng.exponential(1 / 8)

    ship_type = choices(
        [k for k in arrival_probability.keys()],
        [v for v in arrival_probability.values()],
    )

    return (arrive_time, ship_type[0])
