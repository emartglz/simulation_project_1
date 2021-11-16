from simulation import Simulation


def main():
    total_time = 100
    pier_amount = 3
    trailer_amout = 2

    s = Simulation(pier_amount, trailer_amout)
    s.simulate(total_time)
    print(s.Na, s.N_move_pier, s.N_depart_pier, s.N_move_port)


if __name__ == "__main__":
    main()
