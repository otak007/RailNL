from connections import Connection
from stations import Station
from traject import Traject

import random
import csv
import matplotlib.pyplot as plt
import numpy as np
import time

class Map(object):

    def __init__(self):
        self.connections = self.load_connections()
        self.stations = self.load_stations()


    def load_connections(self):
        # Read excel file and create a list with connection objects
        with open('ConnectiesHolland.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            connections = []
            for row in csv_reader:
                connections.append(Connection(row[0], row[1], row[2], False))
            return connections

    def load_stations(self):
        # Read excel file and create a list with station objects
        with open('StationsHolland.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            stations = []

            for row in csv_reader:
                stations.append(Station(row[0], row[1], row[2], row[3]))

            return stations



    def is_critical(self):

        # Checks if connection is connected to critical station
        for station in self.stations:
            for connection in self.connections:
                if (station.name == connection.stationA or station.name == connection.stationB) and station.critical == True:
                    connection.critical = 1


    # Choose random 4 trajects 1000000 times and return the 4 trajects with highest K
    def choose_trajecten(self):


        num_trajects = 3
        trajecten = self.random_traject()

        # Create 4 random different integers
        options = random.sample(range(0, len(trajecten)), num_trajects)

        x = []
        found_kBest = []
        found_k = []

        # Choose 4 trajects twice and rember the 4 with the highest K, repeat this 1 000 000 times
        for i in range(1000000):

            mounted_connections  = []
            traveltime = 0
            mounted_connections_critical = 0

            # Create the total traveltime and total number of mounted critical connections for the first 4 trajects
            for option in options:
                traveltime = traveltime + trajecten[option].total_time
                for connection in trajecten[option].connections:

                    # Add a connection to the list only when it is the first time the connection is mounted.
                    if mounted_connections.count(connection) == 0:
                        mounted_connections.append(connection)
                        mounted_connections_critical = mounted_connections_critical + connection.critical

            k = mounted_connections_critical/20*10000 - (20*num_trajects + traveltime/10)

            # Create the second 4 different random indexes
            options_ = random.sample(range(0, len(trajecten)), num_trajects)

            # create the same variables as the first 4 trajects but now for the second 4 trajects
            mounted_connections_ = []
            traveltime_ = 0
            mounted_connections_critical_ = 0
            for option in options_:
                traveltime_ = traveltime_ + trajecten[option].total_time
                for connection in trajecten[option].connections:
                    if mounted_connections_.count(connection) == 0:
                        mounted_connections_.append(connection)
                        mounted_connections_critical_ = mounted_connections_critical_ + connection.critical
            k_ = mounted_connections_critical_/20*10000 - (20*num_trajects + traveltime_/10)

            found_k.append(k_)


            # remember the best traject
            if k_ > k:
               options = options_
               mounted_connections_critical = mounted_connections_critical_
               k= k_
               traveltime = traveltime_

            # save the founded k
            x.append(i)
            found_kBest.append(k)

        print(trajecten[options[0]].traject)
        print("traveltime ", trajecten[options[0]].total_time)

        print(trajecten[options[1]].traject)
        print("traveltime ", trajecten[options[1]].total_time)

        print(trajecten[options[2]].traject)
        print("traveltime ", trajecten[options[2]].total_time)

        if num_trajects > 3:
            print(trajecten[options[3]].traject)
            print("traveltime ", trajecten[options[3]].total_time)

        print("K: ", k)
        print("Mounted critical connections: ", mounted_connections_critical)
        print("Total traveltime: ", traveltime)

        # plot all the founded K's
        #plt.scatter(x, found_kBest)

        lBins = np.linspace(2000, 10000, num=100)
        plt.hist(found_k, lBins)




    # Create a traject with a random begin station
    def random_traject(self):
        trajecten = []
        for x in range(1000):
            index = random.randint(0, len(self.stations) - 1)
            begin_station = self.stations[index].name
            trajecten.append(self.new_traject(str(x), begin_station, "c"))
        return trajecten

    # Create a new traject
    def new_traject(self, name, station, color):
        traject = Traject(name, station)
        for row in self.stations:
            if station == row.name:
                start_station = row
                break

        return self.travel(traject, start_station, color)



    def travel(self, traject, station, color):
        # Initialize lists
        possible_connections = []
        possible_names = []
        possible_times = []
        possible_critical = []

        self.is_critical()


        # Maximum time is 120 mins
        if traject.total_time < 120:

            # Add relevant connections to relevant lists
            for connection in self.connections:
                if station.name == connection.stationA and connection.travelTime + traject.total_time < 120:
                    possible_names.append(connection.stationB)
                    possible_times.append(connection.travelTime)
                    possible_connections.append(connection)
                    possible_critical.append(connection.critical)

                elif station.name == connection.stationB and connection.travelTime + traject.total_time < 120:
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


            for row in self.stations:
                if next_station == row.name:
                    next_station = row
                    break

            # Reset current station
            traject.traject.append(station.name)
            traject.connections.append(possible_connections[random_index])

            current_station = next_station


            # Travel again with
            self.travel(traject, current_station, color)

        return traject



if __name__ == "__main__":
    NH = Map()
    start = time.time()
    NH.choose_trajecten()
    end = time.time()
    print("CPT: ", end-start)
    plt.show()
