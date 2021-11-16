from averages import calculate_average
from simulation import Simulation


def main():
    total_time = 365 * 24 * 60
    pier_amount = 3
    trailer_amout = 1

    s = Simulation(pier_amount, trailer_amout)
    s.simulate(total_time)

    arrives = {}
    for k in s.A.keys():
        arrives[k] = s.A[k][0]
    print(
        f"average of time in port before go to pier: {calculate_average(s.A_real_depart, arrives)}"
    )
    print(
        f"average of time in move to pier: {calculate_average(s.move_to_pier, s.A_real_depart)}"
    )
    print(
        f"average of time of load in pier: {calculate_average(s.depart, s.move_to_pier)}"
    )
    print(
        f"average of time in pier before go to port: {calculate_average(s.depart_real, s.depart)}"
    )
    print(
        f"average of time in move to port: {calculate_average(s.move_to_port, s.depart_real)}"
    )
    print(f"average of time in total: {calculate_average(s.move_to_port, arrives)}")


if __name__ == "__main__":
    main()
