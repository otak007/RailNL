from code.classes.map import Map
from code.classes.stations import Station
from code.classes.traject import Traject

import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import time
import copy


def is_critical(map, all_critical):

    # Checks if connection is connected to critical station
    for connection in map.connections:
        for station in map.stations:
            if (station.name == connection.stationA or station.name == connection.stationB) and station.critical == True:
                connection.critical = 1

        else:
            if all_critical == "yes":
                connection.critical = 1


# Choose random 4 trajects 1000000 times and return the 4 trajects with highest K
def choose_trajecten(map, max_time, critical, max_trajecten, all_critical):

    num_trajects = 10000
    num_iterations = 100000

    best_trajectory = []

    # Creates and saves random trajecten
    trajecten = random_traject(num_trajects, map, max_time, all_critical)

    # Determine the best k for a train scheduling for each possible
    # number of trajects
    for num_trajects in range(1, num_trajects + 1):
        start = time.time()

        # Create random different integers
        options = random.sample(range(0, len(trajecten)), num_trajects)
        # Creates a list with all founded k-values
        found_k = []

        # Choose the "num_iterations" trajects and remember
        # the trajects with the highest K, repeat this 1 000 000 times
        for i in range(num_iterations):

            mounted_connections  = []
            traveltime = 0
            mounted_connections_critical = 0

            # Create the total traveltime and total number of mounted critical connections for the first train scheduling
            for option in options:
                traveltime = traveltime + trajecten[option].total_time

                for connection in trajecten[option].connections:

                    # Add a connection to the list only when it is the first time the connection is mounted.
                    if mounted_connections.count(connection) == 0:
                        mounted_connections.append(connection)
                        mounted_connections_critical = mounted_connections_critical + connection.critical

            # Calculate the k-value
            k = mounted_connections_critical/critical*10000 - (20*num_trajects + traveltime/10)

            # Create the second random indexes
            options_ = random.sample(range(0, len(trajecten)), num_trajects)

            # create the same variables as the train scheduling but now
            # for the second train schdeduling
            mounted_connections_ = []
            traveltime_ = 0
            mounted_connections_critical_ = 0
            for option in options_:
                traveltime_ = traveltime_ + trajecten[option].total_time
                for connection in trajecten[option].connections:
                    if mounted_connections_.count(connection) == 0:
                        mounted_connections_.append(connection)
                        mounted_connections_critical_ = mounted_connections_critical_ + connection.critical
            k_ = mounted_connections_critical_/critical*10000 - (20*num_trajects + traveltime_/10)

            found_k.append(k_)

            # remember the best traject
            if k_ > k:
               options = options_
               mounted_connections_critical = mounted_connections_critical_
               k = k_
               traveltime = traveltime_


        end = time.time()

        # Save all the founded k-values in an additional file and add at
        # the end of that file the best train scheduling with the best
        # k value
        with open("random_k_resultaten"+str(num_trajects), "w+") as f:
            for foundK in found_k:
                f.write(str(foundK)+ "\n")

            f.write("\nBest traject:\n")
            for i in range(num_trajects):
                best_traject = trajecten[options[i]]
                best_trajectory.append(copy.deepcopy(best_traject))
                f.write(str(trajecten[options[i]].traject)+ "\n")
                f.write(str("traveltime "+ str(trajecten[options[i]].total_time) + "\n"))

            f.write("Total traveltime: " +str(traveltime)+"\n")
            f.write("K: "+ str(k) +"\n")
            f.write("CPT: "+ str(end-start))

    return best_trajectory


# Returns random trajects
def random_traject(num_trajects, map, max_time, all_critical):
    trajecten = []
    for x in range(num_trajects):
        index = random.randint(0, len(map.stations) - 1)
        begin_station = map.stations[index].name
        trajecten.append(new_traject(str(x), begin_station, max_time, map, all_critical))
    return trajecten

# Find a station object given a station name and call travel function
# with the station object
def new_traject(name, station, max_time, map, all_critical):
    traject = Traject(station)
    for row in map.stations:
        if station == row.name:
            start_station = row
            break

    return travel(traject, start_station, max_time, all_critical, map)



def travel(traject, station, max_time, all_critical, map):
    # Initialize lists
    possible_connections = []
    possible_names = []
    possible_times = []
    possible_critical = []


    is_critical(map, all_critical)

    if traject.total_time < max_time:
        # Add relevant connections to relevant lists
        for connection in map.connections:
            if station.name == connection.stationA and connection.travelTime + traject.total_time < max_time:
                possible_names.append(connection.stationB)
                possible_times.append(connection.travelTime)
                possible_connections.append(connection)
                possible_critical.append(connection.critical)

            elif station.name == connection.stationB and connection.travelTime + traject.total_time < max_time:
                possible_names.append(connection.stationA)
                possible_times.append(connection.travelTime)
                possible_connections.append(connection)
                possible_critical.append(connection.critical)

        # return the traject when no other connection is possible to add to the traject
        if len(possible_connections) == 0:
            return;

        # Not possible choose the same connection 2 times in a row, except the station has only 1 connection
        if len(traject.traject) > 0 and len(possible_names) > 1 and possible_names.count(traject.traject[-1]) > 0:
            delete_index = possible_names.index(traject.traject[-1])
            possible_names.pop(delete_index)
            possible_times.pop(delete_index)
            possible_connections.pop(delete_index)

        # Choose random the next station
        random_index = random.randint(0, len(possible_names) - 1)
        next_station = possible_names[random_index]
        traject.total_time += possible_times[random_index]

        # find station object with station name
        for row in map.stations:
            if next_station == row.name:
                next_station = row
                break

        # Add the founded connection to the traject
        traject.traject.append(station.name)
        traject.connections.append(possible_connections[random_index])

        # Travel again with
        travel(traject, next_station, max_time, all_critical, map)

    return traject
