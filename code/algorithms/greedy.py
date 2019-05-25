from code.classes.map import Map
from code.classes.stations import Station
from code.classes.traject import Traject

import csv
import matplotlib.pyplot as plt

def all_stations(color, crit_stations, max_time, map, all_critical):
    ## Goes over all start stations and chooses best traject

    # Initialize lists
    trajecten = []
    scores = []

    # Goes over all start stations
    for x in range(len(map.stations)):

        # Reset critical stations
        is_critical(map, all_critical)


        # Create new traject and travel
        traject = new_traject(map.stations[x].name, "c", crit_stations, max_time, map)
        trajecten.append(traject)
        scores.append(sum(traject.scores))

    # Choose traject with highest score
    index = scores.index(max(scores))
    best_traject = trajecten[index]

    # add connections from best traject to list of already driven connections
    for connection in best_traject.connections:
        map.driven_connections.append(connection.id)

    print(map.driven_connections)
    # add score to total score, subtract 20 as base cost
    map.total_score += sum(best_traject.scores) - 20

    map.scores.append(sum(best_traject.scores))
    map.trajecten.append(best_traject)
    # Plot traject
    plot_traject(best_traject, color, map)

    return best_traject

def new_traject(station, color, crit_stations, max_time, map):

    # Create new traject
    traject = Traject(station)

    # Transform string to object
    for row in map.stations:
        if station == row.name:
            start_station = row
            break

    # Travel from start station
    travel(traject, start_station, color, crit_stations, max_time, map)
    return traject


def is_critical(map, all_critical):

    # Checks if connection is connected to critical station
    for connection in map.connections:
        for station in map.stations:
            if (station.name == connection.stationA or station.name == connection.stationB) and station.critical == True:
                connection.critical = 1

        if map.driven_connections:
            for id in map.driven_connections:
                if id == connection.id:
                    connection.critical = 0
        else:
            if all_critical == "yes":
                connection.critical = 1





def travel(traject, station, color, crit_stations, max_time, map):
    traject_scores = 0

    # Initialize lists
    possible_names = []
    possible_times = []
    possible_scores = []
    possible_connections = []

    # Add relevant connections to relevant lists
    for connection in map.connections:
        if station.name == connection.stationA:
            possible_connections.append(connection)
            possible_names.append(connection.stationB)
            possible_times.append(connection.travelTime)
            possible_scores.append(connection.calc_val(crit_stations))
        elif station.name == connection.stationB:
            possible_connections.append(connection)
            possible_names.append(connection.stationA)
            possible_times.append(connection.travelTime)
            possible_scores.append(connection.calc_val(crit_stations))


    # Looks for best score and according travel time
    best_score = max(possible_scores)
    best_time = possible_times[possible_scores.index(best_score)]

    # If maximum time is not yet exceeded, add fastest connection to traject
    if traject.total_time + best_time <= max_time:

        # Add time to traject total time and score to total score
        traject.total_time += best_time
        traject_scores += best_score
        traject.scores.append(traject_scores)

        # Transform string to station
        index = possible_scores.index(best_score)
        chosen_connection = possible_connections[index]
        next_station = to_station(possible_names[index], map)

        # Set critical (multiplier) to zero)
        for connection in map.connections:
            if (connection == chosen_connection):
                connection.critical = 0

        # Reset current station and add station to traject list
        traject.connections.append(chosen_connection)
        if not traject.traject:
            traject.traject.append(station.name)
        traject.traject.append(next_station.name)

        # Travel again from new station
        travel(traject, next_station, color, crit_stations, max_time, map)

    # If travel time exceeds 120 mins
    else:
        # Remove all unneccessary connections
        remove_unnecessary(traject)
        return traject


def plot_traject(traject, color, map):
    ## plots traject once best traject is chosen

    # goes over every station in traject and plots it
    for x in range(1, len(traject.traject)):
        station1 = to_station(traject.traject[x-1], map)
        station2 = to_station(traject.traject[x], map)

        plt.plot([float(station1.yCoordinate), float(station2.yCoordinate)], [float(station1.xCoordinate), float(station2.xCoordinate)], color+"-")


def remove_unnecessary(traject):
    ## Removes all negative scores at the end of the traject
    counter = 0
    # Repeats as many times as there are scores
    for x in range(1,len(traject.scores)):

        # If last element in list is negative, it's an unnecessary connection and neds to be removed
        if traject.scores[-1] < 0:
            counter += 1
            traject.scores.pop(-1)
            traject.traject.pop(-1)
            traject.connections.pop(-1)
        else:
            return traject

    return traject


def to_station(name, map):
    ## Transforms a station(str) to Station(obj)

    for row in map.stations:
        if name == row.name:
            name = row
            return name
