from code.classes.map import Map
from code.classes.stations import Station
from code.classes.traject import Traject
from code.algorithms.random_trajecten import *

import numpy as np
import csv
import matplotlib.pyplot as plt
import random
import copy
from random import randint


# Simulated Annealing SA

'''
SA randomly deletes the first one or up to 4 connections, and after that
adds one or up to 4 new connections. Or untill the maximum time of 120
min is reached. If this gives a better solution, than that will be accepted.
Otherwise the worse solution is only accepted given a probability depending
on the iterations (temperature) and if hillclimber is false.
The default settings are for Holland. For the whole of the Netherlands
the max number of the trajectory is 180 mins and 89 total of critical
connections.

Arguments:
    trajectories: the linefeeding to optimize
    iteraties_SA: the number of iterations
    num_trajects: the number of trajectories in the linefeeding
    connections: the connections in the graph
    stations: the nodes in the graph
    hillclimber: a boolean for the option to use the hillclimber method

Return:
    A linefeeding with the same number of trajectories.

'''
def SA(trajectories, iteraties_SA, num_trajects, hillclimber, map, max_time, all_critical):
    for i in range(iteraties_SA):
        temp = ((iteraties_SA - i)/(iteraties_SA))*100
        solution_old = copy.deepcopy(trajectories)
        min = 0
        #Choose a traject to change
        x = randint(0, num_trajects - 1)
        # create 4 random different integers of how many connections to delete
        options = random.sample(range(0, 4), 1)
        for i in range(options[0]):
            # if there are more than one stations in the traject remove the first
            if (len(trajectories[x].traject) > 1):
                #remove the first connection by removing the starting station from the list
                strt_station = trajectories[x].traject[0]
                strt_connection = trajectories[x].connections[0]
                trajectories[x].traject.remove(strt_station)
                trajectories[x].connections.remove(strt_connection)
                for connection in map.connections:
                    if ((connection.stationA == strt_station) & (connection.stationB == trajectories[x].traject[0]) ):
                        min = connection.travelTime
                    elif ((connection.stationB == strt_station) & (connection.stationA == trajectories[x].traject[0]) ):
                        min = connection.travelTime
            trajectories[x].total_time -= min
        # creates a random number of how many connections to add to the trajectory
        times = random.sample(range(0, 4), 1)
        times = times[0]
        # create a new solution
        solution_new = travel(trajectories, x, num_trajects, times, max_time, map, all_critical)
        # calculate how much worse the new solution is
        new_K = Calculate_K(solution_new, num_trajects)
        old_K = Calculate_K(solution_old, num_trajects)
        # calculate a probability of accepting a bad solution based on the temperature and the loss
        loss = np.abs((old_K - new_K)*1)
        probability = np.exp(-(loss / temp))
        # take the old solution as the default return solution
        solution = solution_old
        # always accept a better solution
        if (new_K >= old_K):
            solution = solution_new
        # if the solution is worse, there is a chance we take it anyway
        elif (new_K < old_K and (probability > random.random() )) and (hillclimber == False):
            solution = solution_new
        K = Calculate_K(solution, num_trajects)
        print("K is: ", K)
    return solution

'''
Calculate_K calculates the K value of the whole lining for Holland.
For the whole of the Netherlands the total number of critical
connections is 89 and the max traveltime is 180.
'''
def Calculate_K(trajectories, num_trajects):
    tot_num_critical = 20
    mounted_connections  = []
    traveltime = 0
    mounted_connections_critical = 0
    count = 0
    # create the total traveltime and total number of mounted critical connections for the first 4 trajects
    for k in range(num_trajects):
        traveltime = traveltime + trajectories[k].total_time
        for connection in trajectories[k].connections:
            # only unique coinnections will be added
            for i in range(len(mounted_connections)):
                if (mounted_connections[i].stationA == connection.stationA) and ((mounted_connections[i].stationB == connection.stationB)):
                    count += 1
            if (count == 0):
                    mounted_connections.append(connection) if connection not in mounted_connections else mounted_connections
            count = 0
    for connection in mounted_connections:
        mounted_connections_critical = mounted_connections_critical + connection.critical
    k = mounted_connections_critical/tot_num_critical*10000 - (20*num_trajects + traveltime/10)
    return k

'''
Travel receives a trajectory and adds a given number (times) of connections
or untill the maximum of 120 minutes is reached.
'''
def travel(trajectories, x, num_trajects, times, max_time, map, all_critical):
    possible_connections = []
    possible_names = []
    possible_times = []
    possible_critical = []
    # maximum time is 120 mins for only Holland, 180 min for the Netherlands
    traject = trajectories[x]
    is_critical(map, all_critical)
    last = len(traject.traject)
    last_station = traject.traject[last-1]
    if traject.total_time < max_time and times > 0:
        for connection in map.connections:
            if last_station == connection.stationA and connection.travelTime + traject.total_time < max_time:
                possible_names.append(connection.stationB)
                possible_times.append(connection.travelTime)
                possible_connections.append(connection)
                possible_critical.append(connection.critical)
            elif last_station == connection.stationB and connection.travelTime + traject.total_time < max_time:
                possible_names.append(connection.stationA)
                possible_times.append(connection.travelTime)
                possible_connections.append(connection)
                possible_critical.append(connection.critical)
        if len(possible_names) == 0:
            return trajectories;
        # it is not possible choose the same connection 2 times in a row, except the station has only 1 connection
        if len(traject.traject) > 0 and len(possible_names) > 1 and possible_names.count(traject.traject[-1]) > 0:
            delete_index = possible_names.index(traject.traject[-1])
            possible_names.pop(delete_index)
            possible_times.pop(delete_index)
            possible_connections.pop(delete_index)
        # choose random the next station
        random_index = random.randint(0, len(possible_names) - 1)
        next_station = possible_names[random_index]
        traject.total_time += possible_times[random_index]
        traject.traject.append(next_station)
        traject.connections.append(possible_connections[random_index])
        times -= 1
        # travel again until the line is full or the number of times are 0
        travel(trajectories, x, num_trajects, times, max_time, map, all_critical)
    return trajectories
