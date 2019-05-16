from connections import Connection
from stations import Station
from traject import Traject
from random import randint
#from randomTrajecten import Map
import numpy as np

import csv
import matplotlib.pyplot as plt
import random
import copy




# Simulated Annealing SA
class SimulatedAnnealing(object):

    def Calculate_K(trajecten, num_trajects):

        tot_num_critical = 20
        mounted_connections  = []
        traveltime = 0
        mounted_connections_critical = 0

        options = num_trajects
        # Create the total traveltime and total number of mounted critical connections for the first 4 trajects
        for option in range(options):
            traveltime = traveltime + trajecten[option].total_time
            for connection in trajecten[option].connections:

                # Add a connection to the list only when it is the first time the connection is mounted.
                if mounted_connections.count(connection) == 0:
                    mounted_connections.append(connection)
                    mounted_connections_critical = mounted_connections_critical + connection.critical

        k = mounted_connections_critical/tot_num_critical*10000 - (20*num_trajects + traveltime/10)

        return k


    def SA(self, x, trajecten, temp, num_trajects, connections, stations):

        from randomTrajecten import Map

        Solution_current = copy.deepcopy(trajecten)
        min = 0






        #for t in trajecten:
        #    try:
        #        print(t)
        #    except:
        #        print(" ####### ")
        #        t.print_all()
        #        print(t)
        print("het traject:")
        print(trajecten[x].traject)
        if (trajecten[x].traject != None):
            strt_station = trajecten[x].traject[0]
            #start = trajecten[x].traject.remove(strt_station)

            #remove the first connection by removing the starting station from the list
            #del trajecten[x].traject[0]

            # look up the travel time of the first connection
            for connection in connections:
                if ((strt_station == connection.stationA) & (trajecten[x].traject[0] == connection.stationB) ):
                    min = connection.travelTime

            # update the travel time of the traject
            trajecten[x].total_time = trajecten[x].total_time - min

            #the index of the last station
            laatste = len(trajecten[x].traject)-1

            # append new stations from the last station until 120 min are full
            for station in stations:
                if (trajecten[x].traject[laatste] == station.name):
                    station_eind = station

        color = "c"
        Solution_new = copy.deepcopy(trajecten)
        Solution_new[x].traject = Map.travel(self, trajecten[x], station, color)

        # calculate how much worse the new solution is
        loss = SimulatedAnnealing.Calculate_K(Solution_new, num_trajects) - SimulatedAnnealing.Calculate_K(Solution_current, num_trajects)

        # calculate a probability of accepting a bad solution based on the temperature
        # and the loss in K
        probability = np.exp(-(loss / temp))

        # always accept a better solution
        if (SimulatedAnnealing.Calculate_K(Solution_new, num_trajects) < SimulatedAnnealing.Calculate_K(Solution_current, num_trajects)):
            Solution_current = Solution_new

        # not always accept the solution when its worse
        elif (probability > random.random() ):
            Solution_current = Solution_new

        print("de return value")
        print(Solution_current.traject)
        return Solution_current
