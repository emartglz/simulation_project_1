import rng
from enum import Enum


class TrailerSide(Enum):
    port = "port"
    pier = "pier"


def get_move_to_pier_time():
    return rng.exponential(1 / 2)


def get_move_to_port_time():
    return rng.exponential(1)


def get_swap_time():
    return rng.exponential(4)


def move_to_pier(
    ship,
    ship_type,
    trailer,
    pier,
    s,
    login=False,
):
    s.A_real_depart[ship] = s.time
    s.SS_move[trailer] = (ship, pier, TrailerSide.pier)
    s.SS_depart[pier] = ship
    s.time_move_to_pier[trailer] = s.time + get_move_to_pier_time()

    if login:
        print(
            f"Ship {ship} of type {ship_type} going to pier {pier} by trailer {trailer}"
        )


def call_trailer_to_go_to_pier(ship, ship_type, trailer, pier, s, login=False):
    s.SS_move[trailer] = (0, None, TrailerSide.port)
    s.SS_depart[pier] = ship
    s.time_move_to_port[trailer] = s.time + get_swap_time()

    if login:
        print(
            f"Ship {ship} of type {ship_type} call trailer {trailer} from port to go the pier {pier}"
        )


def move_to_port(ship, ship_type, trailer, pier, s, login=False):
    s.depart_real[ship] = s.time
    s.SS_move[trailer] = (ship, 0, TrailerSide.port)
    s.SS_depart[pier] = None
    s.time_move_to_port[trailer] = s.time + get_move_to_port_time()

    if login:
        print(f"Ship {ship} of type {ship_type} going to the port by trailer {trailer}")
