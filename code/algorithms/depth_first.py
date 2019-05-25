from code.classes.map import Map
from code.classes.stations import Station
from code.classes.traject import Traject

import copy
import csv
import matplotlib.pyplot as plt

def all_stations(distance, color, map, all_critical, max_time, crit_stations, steps):

    ## Goes over all start stations and chooses best traject
    is_critical(map, all_critical)

    # Initialize lists
    trajecten = []
    scores = []
    t = []
    s = []

    # Goes over all start stations
    for x in range(len(map.stations)):

        for connection in map.connections:
            connection.travelled = False

        # Create new traject and travel
        traject = Traject(map.stations[x])
        trajects, score = travel(traject, map.stations[x], "y", steps, t, s, map, max_time, crit_stations)
        trajecten.append(copy.deepcopy(trajects))
        scores.append(copy.copy(score))

        t = []
        s = []

    # Choose traject with highest score
    index = scores.index(max(scores))
    best_traject = trajecten[index]

    # add connections from best traject to list of already driven connections
    for connection in best_traject.connections:
        map.driven_connections.append(connection.id)
    map.driven_connections = list(set(map.driven_connections))

    trajecten.append(copy.deepcopy(best_traject))

    # Plot traject
    plot_traject(best_traject, color, distance)

    return best_traject

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


def find_neighbours(station, map):
    # Initialize lists
    connections = []
    stations = []

    # Add relevant connections to relevant lists
    for connection in map.connections:
        if station.name == connection.stationA:
            connections.append(connection)
            stations.append(to_station(connection.stationB, map))
        elif station.name == connection.stationB:
            connections.append(connection)
            stations.append(to_station(connection.stationA, map))

    return connections, stations

def find_subroutes(stations, connections, last_station, steps, traject, t, s, map, max_time, crit_stations, depth = 0, trajecten = [], scores = []):

    # Start with appending start station
    if depth == 0:
        traject.traject.append(last_station)

    # If max depth and time is not reached
    if depth < steps and sum(traject.times) <= max_time:
        # Iterate over stations
        for station in stations:
            # Find connected stations for that station
            connections, stations = find_neighbours(station, map)

            # Go nodes back if max depth is reached
            while len(traject.traject) > (depth + 1):
                lost_connection = traject.connections.pop()
                # If connection no longer travelled, reset variable
                if lost_connection not in traject.connections:
                    lost_connection.travelled = False
                traject.traject.pop()
                traject.times.pop()
                traject.scores.pop()


            # Find connection to node and add to list if possible
            for connection in connections:
                if (last_station.name == connection.stationA and station.name == connection.stationB) or (station.name == connection.stationA and last_station.name == connection.stationB):
                    if sum(traject.times) + connection.travelTime <= max_time:
                        traject.times.append(connection.travelTime)
                        traject.scores.append(connection.calc_val(crit_stations))
                        connection.travelled = True
                        traject.traject.append(station)
                        traject.connections.append(connection)

            # Prevent travelling back
            for next_station in stations:
                if last_station.name is next_station.name:
                    stations.remove(next_station)
                    for connection in connections:
                        if (next_station.name == connection.stationA and station.name == connection.stationB) or (station.name == connection.stationA and next_station.name == connection.stationB):
                            connections.remove(connection)

            # Travel again
            find_subroutes(stations, connections, station, steps, traject, t, s, map, max_time, crit_stations, depth + 1)
    else:

        traject.score = sum(traject.scores)
        traject.time = sum(traject.times)
        t.append(copy.deepcopy(traject))
        s.append(traject.score)



    return t, s

def travel(traject, station, color, steps, t, s, map, max_time, crit_stations):

    connections, stations = find_neighbours(station, map)
    trajecten, scores = find_subroutes(stations, connections, station, steps, traject, t, s, map, max_time, crit_stations)
    best_score = max(scores)


    best_traject = trajecten[scores.index(max(scores))]


    return best_traject, best_score


def plot_traject(traject, color, distance):
    ## plots traject once best traject is chosen

    # goes over every station in traject and plots it
    for x in range(1, len(traject.traject)):
        station1 = traject.traject[x-1]
        station2 = traject.traject[x]

        plt.plot([float(station1.yCoordinate) - 0.02, float(station2.yCoordinate) - 0.02], [float(station1.xCoordinate) + distance * 0.01, float(station2.xCoordinate) + distance * 0.01], color+"-")

def to_station(name, map):
    ## Transforms a station(str) to Station(obj)

    for row in map.stations:
        if name == row.name:
            name = row
            return name
