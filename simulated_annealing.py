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



        # Create the total traveltime and total number of mounted critical connections for the first 4 trajects
        for i in range(num_trajects):
            traveltime = traveltime + trajecten[i].total_time
            for connection in trajecten[i].connections:

                # Add a connection to the list only when it is the first time the connection is mounted.
                if mounted_connections.count(connection) == 0:
                    mounted_connections.append(connection)
                    mounted_connections_critical = mounted_connections_critical + connection.critical

        k = mounted_connections_critical/tot_num_critical*10000 - (20*num_trajects + traveltime/10)

        return k


    def SA(self, x, trajecten, temp, num_trajects, connections, stations):



        K = SimulatedAnnealing.Calculate_K(trajecten, num_trajects)
        from randomTrajectenSA import Map

        Solution_Old = copy.deepcopy(trajecten)
        min = 0

        # Create 4 random different integers
        options = random.sample(range(0, 4), 1)
        print(options)

        #if there are more than one stations in the traject remove the first
        if (len(trajecten[x].traject) > 1):

            #remove the first connection by removing the starting station from the list
            strt_station = trajecten[x].traject[0]
            strt_connection = trajecten[x].connections[0]
            trajecten[x].traject.remove(strt_station)
            trajecten[x].connections.remove(strt_connection)

            # look up the travel time of the first connection
            for connection in connections:
                #print(connection.stationA,  connection.stationB)
                #print(strt_station, trajecten[x].traject[0])
                if ((connection.stationA == strt_station) & (connection.stationB == trajecten[x].traject[0]) ):
                    min = connection.travelTime
                elif ((connection.stationB == strt_station) & (connection.stationA == trajecten[x].traject[0]) ):
                    min = connection.travelTime

        #print("Min: ", min)
        # update the travel time of the traject

        trajecten[x].total_time -= min

        #get the index of the last station
        #laatste = len(trajecten[x].traject)-1

        # get the name of the first station
        for station in stations:
            if trajecten[x].traject[0] == station.name:
                station_eind = station
                break

        # add a new station to the traject

        Solution_New = SimulatedAnnealing.travel(self, trajecten, x, connections, stations, num_trajects)


        #trajecten[x].print_all()

        # calculate how much worse the new solution is
        New_K = SimulatedAnnealing.Calculate_K(Solution_New, num_trajects)
        Old_K = SimulatedAnnealing.Calculate_K(Solution_Old, num_trajects)

        loss = np.abs((Old_K - New_K)*1)
        # calculate a probability of accepting a bad solution based on the temperature
        # and the loss in K
        probability = np.exp(-(loss / temp))
        #print("Kans om een slechtere K aan te nemen: ", probability)
        # Take the old solution as the default return solution
        Solution = Solution_Old

        # always accept a better solution, so Solution_New is the default return value
        # If the new solution is better, take that one
        if (New_K >= Old_K):
            Solution = Solution_New
        # Or if the solution is worse, there is a chance we take it anyway
        elif (New_K < Old_K and (probability > random.random() )):
            Solution = Solution_New



        K = SimulatedAnnealing.Calculate_K(Solution, num_trajects)
        return Solution



    def travel(self, trajecten, x, connections, stations, num_trajects):
        # Initialize lists
        possible_connections = []
        possible_names = []
        possible_times = []
        possible_critical = []

        traject = trajecten[x]

        self.is_critical()

        max_min = 120

        last = len(traject.traject)
        last_station = traject.traject[last-1]
        #print("0:TRAJECT:", traject, "STATION: ", station.name)
        # Maximum time is 120 mins
        if traject.total_time < max_min:

            # Add relevant connections to relevant lists
            for connection in connections:
                if last_station == connection.stationA and connection.travelTime + traject.total_time < max_min:
                    possible_names.append(connection.stationB)
                    possible_times.append(connection.travelTime)
                    possible_connections.append(connection)
                    possible_critical.append(connection.critical)
                elif last_station == connection.stationB and connection.travelTime + traject.total_time < max_min:
                    possible_names.append(connection.stationA)
                    possible_times.append(connection.travelTime)
                    possible_connections.append(connection)
                    possible_critical.append(connection.critical)


            # return the traject when no other connection is possible to add to the traject
            if len(possible_names) == 0:
                return trajecten;
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


            # Reset current station
            traject.traject.append(next_station)
            traject.connections.append(possible_connections[random_index])

            # Travel again with
            SimulatedAnnealing.travel(self, trajecten, x, connections, stations, num_trajects)


        return trajecten
