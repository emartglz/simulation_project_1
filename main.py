from simulation import Simulation


def main():
    total_time = 100
    pier_amount = 3
    trailer_amout = 2

    s = Simulation(pier_amount, trailer_amout)
    s.simulate(total_time)


if __name__ == "__main__":
    main()
