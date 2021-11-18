from averages import calculate_average
from simulation import Simulation
from matplotlib import pyplot as plt
import numpy as np


def multiples_simulations(total_time, pier_amount, trailer_amount, simulation_amount):
    average_time_in_port = []
    average_time_move_to_pier = []
    average_time_of_load = []
    average_time_in_pier_after_load = []
    average_time_move_to_port = []
    average_time_total = []
    for _ in range(simulation_amount):
        s = Simulation(pier_amount, trailer_amount)
        s.simulate(total_time)

        arrives = {}
        for k in s.A.keys():
            arrives[k] = s.A[k][0]

        average_time_in_port.append(calculate_average(s.A_real_depart, arrives))
        average_time_move_to_pier.append(
            calculate_average(s.move_to_pier, s.A_real_depart)
        )
        average_time_of_load.append(calculate_average(s.depart, s.move_to_pier))
        average_time_in_pier_after_load.append(
            calculate_average(s.depart_real, s.depart)
        )
        average_time_move_to_port.append(
            calculate_average(s.move_to_port, s.depart_real)
        )
        average_time_total.append(calculate_average(s.move_to_port, arrives))

        print(f"time in total: {average_time_total[-1]}")

    plt.figure(figsize=(8, 8))
    plt.subplots_adjust(bottom=0.5)
    plt.plot(
        [0 for _ in range(len(average_time_in_port))],
        average_time_in_port,
        "x",
    )
    plt.plot(
        [1 for _ in range(len(average_time_move_to_pier))],
        average_time_move_to_pier,
        "x",
    )
    plt.plot(
        [2 for _ in range(len(average_time_of_load))],
        average_time_of_load,
        "x",
    )
    plt.plot(
        [3 for _ in range(len(average_time_in_pier_after_load))],
        average_time_in_pier_after_load,
        "x",
    )
    plt.plot(
        [4 for _ in range(len(average_time_move_to_port))],
        average_time_move_to_port,
        "x",
    )
    plt.plot(
        [5 for _ in range(len(average_time_total))],
        average_time_total,
        "x",
    )
    plt.ylabel("minutes")
    plt.xlabel("averages")
    plt.xticks(
        np.arange(6),
        [
            "time in port before go to pier",
            "time in move to pier",
            "time of load in pier",
            "time in pier before go to port",
            "time in move to port",
            "time in total",
        ],
        rotation="vertical",
    )
    plt.savefig(
        f"simulation_{total_time}_{pier_amount}_{trailer_amount}_{simulation_amount}.pdf"
    )


def main():
    total_time = 365 * 24 * 60
    pier_amount = 3
    trailer_amout = 1
    simulation_amount = 10

    multiples_simulations(total_time, pier_amount, trailer_amout, simulation_amount)


if __name__ == "__main__":
    main()
