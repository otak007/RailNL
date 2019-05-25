import code.algorithms.greedy as greedy
import code.algorithms.random_trajecten as random
import code.algorithms.simulated_annealing as sim
import code.classes.map as maps
import code.algorithms.depth_first as depth

import csv
import matplotlib.pyplot as plt
import time

if __name__ == "__main__":

    response = (input("Which map do you want to run? Holland or NL?\n")).lower()

    while response != "holland" and response != "nl":
        response = input("Choose holland or nl\n").lower()

    if response == 'holland':
        map = "Holland"
        max_time = 120
        max_trajecten = 7
        all_critical = input("Type 'yes' if you want all stations critical.\n").lower()
        if all_critical == "yes":
            critical_stations = 28
        else:
            critical_stations = 20
    elif response == "nl":
        map = "Nationaal"
        max_time = 180
        max_trajecten = 20
        all_critical = input("Type 'yes' if you want all stations critical.\n").lower()
        if all_critical == "yes":
            critical_stations = 89
        else:
            critical_stations = 59

    data = maps.Map(map, all_critical)

    response = input("""Press 1 to run greedy algorithm.\n
Press 2 to run random algorithm.\n
Press 3 to run simulated annealing.\n
Press 4 to run depth first algorithm.\n""")

    while response != '1' and response != '2' and response != '3' and response != '4':
        response = input("Please choose a number from 1-4\n")

    colors = ['b', 'g', 'r', 'k', 'c', 'm']
    start = time.time()

    if response == '1':
        iterations = int(input("How many trajectories would you like?\n"))

        score = 0
        trajecten = []

        while int(iterations) > max_trajecten:
            iterations = input("No more than " + str(max_trajecten) + " trajectories.\n")

        for x in range(0, int(iterations)):

            traject = greedy.all_stations(colors[x % 6], critical_stations, max_time, data, all_critical)
            trajecten.append(traject)
            score += sum(traject.scores) - 20

            print("Traject nr. " + str(x + 1) + ": " + ', '.join(traject.traject))
            print(traject.total_time)
            print(str(traject.scores) + "\n")

        print("Total K: " + str(score))
        end = time.time()
        print("Time: " + str(end - start))
        plt.show()

    elif response == '2':

        random.choose_trajecten(data, max_time, critical_stations, max_trajecten, all_critical)

        print("Time: " + str(end - start))

    elif response == '3':

        start_traject = random.choose_trajecten(data, max_time, critical_stations, max_trajecten, all_critical)

        iterations = int(input("How many iterations would you like?\n"))

        if iterations > 0:
            hillclimber = input("Activate hillclimber? Y or n\n").lower()
            while hillclimber != 'y' and hillclimber != 'n':
                hillclimber = input("Please type y or n\n")
            if hillclimber == 'y':
                hillclimber = True
            elif hillclimber == 'n':
                hillclimber = False
            sim.SA(start_traject, iterations, len(start_traject), hillclimber, data, max_time, all_critical)

        print("Time: " + str(end - start))

    elif response == '4':
        iterations = int(input("How many trajectories would you like?\n"))
        steps = int(input("How many nodes would you like to go deep?\n"))

        score = 0
        trajecten = []

        while int(iterations) > max_trajecten:
            iterations = input("No more than " + str(max_trajecten) + " trajectories.\n")

        for x in range(0, int(iterations)):
            traject = depth.all_stations(x * 0.5, colors[x % 6], data, all_critical, max_time, critical_stations, steps)
            trajecten.append(traject)
            score += sum(traject.scores) - 20

            print(traject.total_time)
            print(str(traject.scores) + "\n")

        print("Total K: " + str(score))
        end = time.time()
        print("Time: " + str(end - start))
        plt.show()
