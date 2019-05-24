
from connectionsSander import Connection
from stations import Station
from trajectSander import Traject

import copy
import csv
import matplotlib.pyplot as plt

class Map(object):

    def __init__(self):
        self.connections = self.load_connections()
        self.stations = self.load_stations()
        self.total_score = 0
        self.trajecten = []
        self.scores = []
        self.times = []
        self.driven_connections = []

    def load_connections(self):
        # Read excel file and create a list with connection objects
        with open('C:/Users/User/Documents/Programmeertheorie/RailNL/data/ConnectiesHolland.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            connections = []
            for row in csv_reader:
                connections.append(Connection(csv_reader.line_num, row[0], row[1], row[2]))
            return connections

    def load_stations(self):
        # Read excel file and create a list with station objects
        with open('C:/Users/User/Documents/Programmeertheorie/RailNL/data/StationsHolland.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            stations = []

            for row in csv_reader:
                stations.append(Station(row[0], row[1], row[2], row[3]))
                plt.plot(float(row[2]), float(row[1]), "bo")
                plt.text(float(row[2]) -0.02, float(row[1])+0.02, row[0], fontsize=5)
            return stations

    def is_critical(self):

        # Checks if connection is connected to critical station
        for station in self.stations:
            for connection in self.connections:

                if self.driven_connections:

                    for driven in self.driven_connections:
                        if connection.id == driven:
                            connection.critical = 0
                else:
                    connection.critical = 1

    def plot(self):

        for station in self.stations:
            for connection in self.connections:
                if station.name == connection.stationA or station.name == connection.stationB:
                   for station2 in self.stations:
                       if station2.name == connection.stationB or station2.name == connection.stationA:
                           plt.plot([float(station.yCoordinate), float(station2.yCoordinate)], [float(station.xCoordinate), float(station2.xCoordinate)], 'y-')

    def find_neighbours(self, station):
        # Initialize lists
        connections = []
        stations = []

        # Add relevant connections to relevant lists
        for connection in self.connections:
            if station.name == connection.stationA:
                connections.append(connection)
                stations.append(self.to_station(connection.stationB))
            elif station.name == connection.stationB:
                connections.append(connection)
                stations.append(self.to_station(connection.stationA))

        return connections, stations

    def find_subroutes(self, stations, connections, last_station, steps, traject, t, s, depth = 0, trajecten = [], scores = []):

        # Start with appending start station
        if depth == 0:
            traject.traject.append(last_station)

        # If max depth and time is not reached
        if depth < steps and sum(traject.times) <= 120:
            # Iterate over stations
            for station in stations:
                # Find connected stations for that station
                connections, stations = self.find_neighbours(station)

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
                        if sum(traject.times) + connection.travelTime <= 120:
                            traject.times.append(connection.travelTime)
                            traject.scores.append(connection.calc_val())
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
                self.find_subroutes(stations, connections, station, steps, traject, t, s, depth + 1)
        else:

            traject.score = sum(traject.scores)
            traject.time = sum(traject.times)
            t.append(copy.deepcopy(traject))
            s.append(traject.score)



        return t, s

    def travel(self, traject, station, color, steps, t, s):

        connections, stations = self.find_neighbours(station)
        trajecten, scores = self.find_subroutes(stations, connections, station, steps, traject, t, s)
        best_score = max(scores)


        best_traject = trajecten[scores.index(max(scores))]


        return best_traject, best_score

    def all_stations(self, distance, color, steps = 1):

        ## Goes over all start stations and chooses best traject
        self.is_critical()

        # Initialize lists
        trajecten = []
        scores = []
        t = []
        s = []

        # Goes over all start stations
        for x in range(len(self.stations)):

            for connection in self.connections:
                connection.travelled = False

            # Create new traject and travel
            traject = Traject(self.stations[x])
            trajects, score = self.travel(traject, self.stations[x], "y", steps, t, s)
            trajecten.append(copy.copy(trajects))
            scores.append(copy.copy(score))

            t = []
            s = []

        # Choose traject with highest score
        index = scores.index(max(scores))
        best_traject = trajecten[index]

        # add connections from best traject to list of already driven connections
        for connection in best_traject.connections:
            self.driven_connections.append(connection.id)
        self.driven_connections = list(set(self.driven_connections))

        # add score to total score, subtract 20 as base cost
        self.total_score += sum(best_traject.scores) - 20

        self.trajecten.append(best_traject)

        # Plot traject
        self.plot_traject(best_traject, color, distance)

    def plot_traject(self, traject, color, distance):
        ## plots traject once best traject is chosen

        # goes over every station in traject and plots it
        for x in range(1, len(traject.traject)):
            station1 = traject.traject[x-1]
            station2 = traject.traject[x]

            plt.plot([float(station1.yCoordinate) - 0.02, float(station2.yCoordinate) - 0.02], [float(station1.xCoordinate) + distance * 0.01, float(station2.xCoordinate) + distance * 0.01], color+"-")

    def to_station(self, name):
        ## Transforms a station(str) to Station(obj)

        for row in self.stations:
            if name == row.name:
                name = row
                return name

if __name__ == "__main__":
    # Initialize map, plot and give four starting stations
    NH = Map()
    NH.plot()
    NH.all_stations(0.5, "b", 2)
    plt.show()
