from port import generate_arrive
from trailer import (
    call_trailer_to_go_to_pier,
    get_swap_time,
    TrailerSide,
    move_to_pier,
    move_to_port,
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


class Simulation:
    def __init__(self, pier_amount, trailer_amount):
        self.pier_amount = pier_amount
        self.trailer_amount = trailer_amount

        self.SS_move = [
            (None, None, TrailerSide.port) for _ in range(trailer_amount)
        ]  # status of trailers trailer_number : (ship being moved, pier of destiny, side of trailer)

        self.SS_depart = [None for _ in range(trailer_amount)]  # status of piers
        self.time_move_to_pier = [
            INF for _ in range(trailer_amount)
        ]  # list of times of trailers to arrive to his pier destination
        self.time_depart_pier = [
            INF for _ in range(pier_amount)
        ]  # list of times of piers to complete the load
        self.time_move_to_port = [
            INF for _ in range(trailer_amount)
        ]  # list of times of trailers to arrive to his port destination

    time = 0  # time
    Na = 0  # number of ships arrived
    N_move_pier = 0  # number of ships moved to pier
    N_depart_pier = 0  # number of ships departed from pier
    N_move_port = 0  # number of ships moved to port

    A = {}  # all the ships arrived ship_number : (time, ship_type)
    A_real_depart = {}  # real ship depart time from port

    move_to_pier = {}  # time of ship arrive to pier

    depart = {}  # time of ship should depart pier
    depart_real = {}  # real time of ship depart pier

    move_to_port = {}  # time of ship arrive to port to leave

    SS_move_to_pier_queue = []  # queue of ships waiting to go to pier

    SS_move_to_port_queue = []  # queue of ships waiting to go to port

    def simulate(self, total_time, login=False):

        time_arrive = 0

        while (
            min(
                time_arrive,
                min_of_list(self.time_move_to_pier),
                min_of_list(self.time_depart_pier),
                min_of_list(self.time_move_to_port),
            )
            != INF
        ):
            if login:
                print()
                print(f"SS_move: {self.SS_move}")
                print(f"SS_depart: {self.SS_depart}")
                print(f"pier_queue: {self.SS_move_to_pier_queue}")
                print(f"port queue: {self.SS_move_to_port_queue}")
                print(f"time: {self.time}")
                print()

            # Arrive event
            if (
                min(
                    time_arrive,
                    min_of_list(self.time_move_to_pier),
                    min_of_list(self.time_depart_pier),
                    min_of_list(self.time_move_to_port),
                )
                == time_arrive
            ):
                self.time = time_arrive

                arrive = generate_arrive()
                time_arrive_temp = arrive[0]
                time_arrive = self.time + time_arrive_temp
                ship_arrive_type = arrive[1]

                if self.time == 0:  # First iteration
                    continue

                self.Na += 1
                ship = self.Na
                self.A[ship] = (self.time, ship_arrive_type)

                # no more generation of arrives
                if time_arrive > total_time:
                    time_arrive = INF

                if login:
                    print(f"Ship {ship} of type {ship_arrive_type} arrive to the port")

                trailer_free = get_first_none_tuple(self.SS_move, TrailerSide.port)
                trailer_free_other_side = get_first_none_tuple(
                    self.SS_move, TrailerSide.pier
                )
                pier_free = get_first_none(self.SS_depart)

                # going to pier
                if (
                    len(self.SS_move_to_pier_queue) == 0
                    and trailer_free is not None
                    and pier_free is not None
                ):
                    move_to_pier(
                        ship, ship_arrive_type, trailer_free, pier_free, self, login
                    )

                # calling trailer from pier to port
                elif (
                    len(self.SS_move_to_pier_queue) == 0
                    and trailer_free_other_side is not None
                    and pier_free
                ):
                    call_trailer_to_go_to_pier(
                        ship,
                        ship_arrive_type,
                        trailer_free_other_side,
                        self,
                        login,
                    )
                    self.SS_move_to_pier_queue.append(ship)

                    if login:
                        print(
                            f"Ship {ship} of type {ship_arrive_type} going to queue to go to the pier"
                        )

                # goin to queue
                else:
                    self.SS_move_to_pier_queue.append(ship)

                    if login:
                        print(
                            f"Ship {ship} of type {ship_arrive_type} going to queue to go to the pier"
                        )

            # Move to Pier
            elif (
                min(
                    time_arrive,
                    min_of_list(self.time_move_to_pier),
                    min_of_list(self.time_depart_pier),
                    min_of_list(self.time_move_to_port),
                )
                == min_of_list(self.time_move_to_pier)
            ):
                trailer = get_position_of_min(self.time_move_to_pier)
                ship, pier, _ = self.SS_move[trailer]
                self.time = self.time_move_to_pier[trailer]
                self.time_move_to_pier[trailer] = INF
                self.SS_move[trailer] = (None, None, TrailerSide.pier)

                # not was a swap
                if pier is not None:
                    ship_type = self.A[ship][1]
                    self.N_move_pier += 1
                    self.move_to_pier[ship] = self.time

                    self.time_depart_pier[pier] = self.time + get_load_time(ship_type)

                    if login:
                        print(
                            f"Ship {ship} of type {ship_type} arrive to the pier {pier} by trailer {trailer}"
                        )

                # is a swap
                else:
                    if login:
                        print(f"Trailer {trailer} arrive to pier by swap")

                pier_free = get_first_none(self.SS_depart)

                # ship ready to depart going to port
                if len(self.SS_move_to_port_queue) > 0:
                    ship_leave, pier_leave = self.SS_move_to_port_queue.pop()
                    move_to_port(
                        ship_leave,
                        self.A[ship_leave][1],
                        trailer,
                        pier_leave,
                        self,
                        login,
                    )

                # ship in port and pier free bring a ship to pier
                elif pier_free is not None and len(self.SS_move_to_pier_queue) > 0:
                    ship_to_come = self.SS_move_to_pier_queue[0]
                    call_trailer_to_go_to_pier(
                        ship_to_come,
                        self.A[ship_to_come][1],
                        trailer,
                        self,
                        login,
                    )

            # Depart Pier
            elif (
                min(
                    time_arrive,
                    min_of_list(self.time_move_to_pier),
                    min_of_list(self.time_depart_pier),
                    min_of_list(self.time_move_to_port),
                )
                == min_of_list(self.time_depart_pier)
            ):
                pier = get_position_of_min(self.time_depart_pier)
                ship = self.SS_depart[pier]
                ship_type = self.A[ship][1]
                self.time = self.time_depart_pier[pier]
                self.time_depart_pier[pier] = INF

                self.N_depart_pier += 1
                self.depart[ship] = self.time

                if login:
                    print(
                        f"Ship {ship} of type {ship_type} is ready to depart from pier {pier}"
                    )

                trailer_free = get_first_none_tuple(self.SS_move, TrailerSide.pier)

                # ship ready to depart, going to port
                if trailer_free is not None and len(self.SS_move_to_port_queue) == 0:
                    move_to_port(ship, ship_type, trailer_free, pier, self, login)

                # going to queue
                else:
                    self.SS_move_to_port_queue.append((ship, pier))

                    if login:
                        print(
                            f"Ship {ship} of type {ship_type} going to queue to go to port"
                        )

            # Move to Port
            elif (
                min(
                    time_arrive,
                    min_of_list(self.time_move_to_pier),
                    min_of_list(self.time_depart_pier),
                    min_of_list(self.time_move_to_port),
                )
                == min_of_list(self.time_move_to_port)
            ):
                trailer = get_position_of_min(self.time_move_to_port)
                ship, pier, _ = self.SS_move[trailer]
                self.time = self.time_move_to_port[trailer]
                self.time_move_to_port[trailer] = INF
                self.SS_move[trailer] = (None, 0, TrailerSide.port)

                # is not a swap
                if pier is not None:
                    ship_type = self.A[ship][1]
                    self.N_move_port += 1
                    self.move_to_port[ship] = self.time

                    if login:
                        print(
                            f"Ship {ship} of type {ship_type} arrive to the port by trailer {trailer}"
                        )

                # is a swap
                else:
                    if login:
                        print(f"Trailer {trailer} arrive to port by swap")

                pier_free = get_first_none(self.SS_depart)
                # ships ready to go to pier
                if len(self.SS_move_to_pier_queue) > 0 and pier_free is not None:
                    ship_bring = self.SS_move_to_pier_queue.pop(0)
                    ship_bring_type = self.A[ship_bring][1]

                    move_to_pier(
                        ship_bring, ship_bring, trailer, pier_free, self, login
                    )

                # going to pier to help ships
                elif not is_full_none(self.SS_depart):
                    self.SS_move[trailer] = (0, None, TrailerSide.pier)
                    self.time_move_to_pier[trailer] = self.time + get_swap_time()

                    if login:
                        print(
                            f"Trailer {trailer} swap to pier for help rest of ships in pier"
                        )
