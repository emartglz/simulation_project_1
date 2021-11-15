from port import generate_arrive
from functools import reduce
from trailer import (
    get_move_to_port_time,
    get_move_to_pier_time,
    get_swap_time,
    TrailerSide,
)
from ship import get_load_time
from macros import INF
from utils import (
    get_first_none,
    get_first_none_tuple,
    get_position_of_min,
    is_full_none,
    min_of_list,
)


def simulate(total_time, pier_amount, trailer_amout):
    time = 0  # time
    Na = 0  # number of ships arrived
    N_move_pier = 0  # number of ships moved to pier
    N_depart_pier = 0  # number of ships departed from pier
    N_move_port = 0  # number of ships moved to port

    A = {}  # all the ships arrived ship_number : (time, ship_type)
    A_real_dpart = {}  # real ship depart time from port

    move_to_pier = {}  # time of ship arrive to pier

    depart = {}  # time of ship should depart pier
    depart_real = {}  # real time of ship depart pier

    move_to_port = {}  # time of ship arrive to port to leave

    #           Na,pier of destiny,Side,
    SS_move = [
        (None, None, TrailerSide.port) for _ in range(trailer_amout)
    ]  # status of trailers trailer_number : (ship being moved, pier of destiny, side of trailer)
    SS_move_to_pier_queue = []  # queue of ships waiting to go to pier

    SS_depart = [None for _ in range(pier_amount)]  # status of piers

    SS_move_to_port_queue = []  # queue of ships waiting to go to port

    time_move_to_pier = [
        INF for _ in range(trailer_amout)
    ]  # list of times of trailers to arrive to his pier destination
    time_depart_pier = [
        INF for _ in range(pier_amount)
    ]  # list of times of piers to complete the load
    time_move_to_port = [
        INF for _ in range(trailer_amout)
    ]  # list of times of trailers to arrive to his port destination

    time_arrive = 0

    while (
        min(
            time_arrive,
            min_of_list(time_move_to_pier),
            min_of_list(time_depart_pier),
            min_of_list(time_move_to_port),
        )
        != INF
    ):
        # temp = input()
        print()
        print(f"SS_move: {SS_move}")
        print(f"SS_depart: {SS_depart}")
        print(f"pier_queue: {SS_move_to_pier_queue}")
        print(f"port queue: {SS_move_to_port_queue}")
        print(f"time: {time}")
        print()

        # Arrive event
        if (
            min(
                time_arrive,
                min_of_list(time_move_to_pier),
                min_of_list(time_depart_pier),
                min_of_list(time_move_to_port),
            )
            == time_arrive
        ):
            time = time_arrive

            arrive = generate_arrive()
            time_arrive_temp = arrive[0]
            time_arrive = time + time_arrive_temp
            ship_arrive_type = arrive[1]

            if time == 0:  # First iteration
                continue

            Na += 1
            ship = Na
            A[ship] = (time, ship_arrive_type)

            if time_arrive > total_time:
                time_arrive = INF

            print(f"Ship {ship} of type {ship_arrive_type} arrive to the port")

            trailer_free = get_first_none_tuple(SS_move, TrailerSide.port)
            trailer_free_other_side = get_first_none_tuple(SS_move, TrailerSide.pier)
            pier_free = get_first_none(SS_depart)

            # going to pier
            if (
                len(SS_move_to_pier_queue) == 0
                and trailer_free is not None
                and pier_free is not None
            ):
                A_real_dpart[ship] = time
                SS_move[trailer_free] = (ship, pier_free, TrailerSide.pier)
                SS_depart[pier_free] = ship
                time_move_to_pier[trailer_free] = time + get_move_to_pier_time()

                print(
                    f"Ship {ship} of type {ship_arrive_type} going to pier {pier_free} by trailer {trailer_free}"
                )

            # calling trailer from pier to port
            elif (
                len(SS_move_to_pier_queue) == 0
                and trailer_free_other_side is not None
                and pier_free
            ):
                SS_move[trailer_free_other_side] = (0, None, TrailerSide.port)
                SS_depart[pier_free] = ship
                time_move_to_port[trailer_free_other_side] = time + get_swap_time()
                SS_move_to_pier_queue.append(ship)

                print(
                    f"Ship {ship} of type {ship_arrive_type} call trailer {trailer_free_other_side} from port to go the pier {pier_free}"
                )

            # goin to queue
            else:
                SS_move_to_pier_queue.append(ship)

                print(
                    f"Ship {ship} of type {ship_arrive_type} going to queue to go to the pier"
                )

        # Move to Pier
        elif (
            min(
                time_arrive,
                min_of_list(time_move_to_pier),
                min_of_list(time_depart_pier),
                min_of_list(time_move_to_port),
            )
            == min_of_list(time_move_to_pier)
        ):
            trailer = get_position_of_min(time_move_to_pier)
            ship, pier, _ = SS_move[trailer]
            time = time_move_to_pier[trailer]
            time_move_to_pier[trailer] = INF
            SS_move[trailer] = (None, None, TrailerSide.pier)

            # not was a swap
            if pier is not None:
                N_move_pier += 1
                move_to_pier[ship] = time

                time_depart_pier[pier] = time + get_load_time(A[ship][1])

                print(
                    f"Ship {ship} of type {A[ship][1]} arrive to the pier {pier} by trailer {trailer}"
                )

            # is a swap
            else:
                print(f"Trailer {trailer} arrive to pier by swap")

            pier_free = get_first_none(SS_depart)

            # ship ready to depart going to port
            if len(SS_move_to_port_queue) > 0:
                ship_leave, pier_leave = SS_move_to_port_queue.pop()
                depart_real[ship_leave] = time
                SS_move[trailer] = (ship_leave, 0, TrailerSide.port)
                SS_depart[pier_leave] = None
                time_move_to_port[trailer] = time + get_move_to_port_time()

                print(
                    f"Ship {ship_leave} of type {A[ship_leave][1]} going to the port by trailer {trailer}"
                )

            # ship in port and pier free bring a ship to pier
            elif pier_free is not None and len(SS_move_to_pier_queue) > 0:
                SS_move[trailer] = (0, None, TrailerSide.port)
                SS_depart[pier_free] = SS_move_to_pier_queue[0]
                time_move_to_port[trailer] = time + get_swap_time()

                print(
                    f"Ship {SS_move_to_pier_queue[0]} of type {A[SS_move_to_pier_queue[0]][1]} call trailer {trailer} from port to go the pier {pier_free}"
                )

        # Depart Pier
        elif (
            min(
                time_arrive,
                min_of_list(time_move_to_pier),
                min_of_list(time_depart_pier),
                min_of_list(time_move_to_port),
            )
            == min_of_list(time_depart_pier)
        ):
            pier = get_position_of_min(time_depart_pier)
            ship = SS_depart[pier]
            time = time_depart_pier[pier]
            time_depart_pier[pier] = INF

            N_depart_pier += 1
            depart[ship] = time

            print(
                f"Ship {ship} of type {A[ship][1]} is ready to depart from pier {pier}"
            )

            trailer_free = get_first_none_tuple(SS_move, TrailerSide.pier)

            # ship ready to depart, going to port
            if trailer_free is not None and len(SS_move_to_port_queue) == 0:
                depart_real[ship] = time
                SS_move[trailer_free] = (ship, 0, TrailerSide.port)
                SS_depart[pier] = None
                time_move_to_port[trailer_free] = time + get_move_to_port_time()

                print(
                    f"Ship {ship} of type {A[ship][1]} going to the port by trailer {trailer_free}"
                )

            # going to queue
            else:
                SS_move_to_port_queue.append((ship, pier))

                print(f"Ship {ship} of type {A[ship][1]} going to queue to go to port")

        # Move to Port
        elif (
            min(
                time_arrive,
                min_of_list(time_move_to_pier),
                min_of_list(time_depart_pier),
                min_of_list(time_move_to_port),
            )
            == min_of_list(time_move_to_port)
        ):
            trailer = get_position_of_min(time_move_to_port)
            ship, pier, _ = SS_move[trailer]
            time = time_move_to_port[trailer]
            time_move_to_port[trailer] = INF
            SS_move[trailer] = (None, 0, TrailerSide.port)

            # is not a swap
            if pier is not None:
                N_move_port += 1
                move_to_port[ship] = time

                print(
                    f"Ship {ship} of type {A[ship][1]} arrive to the port by trailer {trailer}"
                )

            # is a swap
            else:
                print(f"Trailer {trailer} arrive to port by swap")

            pier_free = get_first_none(SS_depart)
            # ships ready to go to pier
            if len(SS_move_to_pier_queue) > 0:
                # with reservation
                if SS_move_to_pier_queue[0] in SS_depart:
                    ship_bring = SS_move_to_pier_queue.pop(0)
                    pier_reserved = SS_depart.index(ship_bring)
                    A_real_dpart[ship_bring] = time
                    SS_move[trailer] = (ship_bring, pier_reserved, TrailerSide.pier)
                    time_move_to_pier[trailer] = time + get_move_to_pier_time()

                    print(
                        f"Ship {ship_bring} of type {A[ship_bring][1]} going to pier {pier_reserved} by trailer {trailer}"
                    )

                    continue

                # without reservation but pier free
                elif pier_free is not None:
                    ship_bring = SS_move_to_pier_queue.pop(0)
                    A_real_dpart[ship_bring] = time
                    SS_depart[pier_free] = ship_bring
                    SS_move[trailer] = (ship_bring, pier_free, TrailerSide.pier)
                    time_move_to_pier[trailer] = time + get_move_to_pier_time()

                    print(
                        f"Ship {ship_bring} of type {A[ship_bring][1]} going to pier {pier_free} by trailer {trailer}"
                    )
                    continue

            # going to pier to help ships (this is my asumption)
            if not is_full_none(SS_depart):
                SS_move[trailer] = (0, None, TrailerSide.pier)
                time_move_to_pier[trailer] = time + get_swap_time()

                print(f"Trailer {trailer} swap to pier for help rest of ships in pier")
