from connections import Connection
from stations import Station
from traject import Traject

import csv
import matplotlib.pyplot as plt

class Map(object):

    def __init__(self):
        self.connections = self.load_connections()
        self.stations = self.load_stations()
        self.is_critical()
        self.total_score = 0

    def load_connections(self):
        # Read excel file and create a list with connection objects
        with open('data/ConnectiesHolland.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            connections = []
            for row in csv_reader:
                connections.append(Connection(row[0], row[1], row[2], False))
            return connections

    def load_stations(self):
        # Read excel file and create a list with station objects
        with open('data/StationsHolland.csv') as csv_file:
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
                if (station.name == connection.stationA or station.name == connection.stationB) and station.critical == True:
                    connection.critical = 1

    def plot(self):

        for station in self.stations:

            for connection in self.connections:

                if (station.name == connection.stationA or station.name == connection.stationB) and connection.chooseConnection == False:
                   connection.chooseConnection = True

                   for station2 in self.stations:
                       if station2.name == connection.stationB or station2.name == connection.stationA:
                           if station.critical or station2.critical:
                               plt.plot([float(station.yCoordinate), float(station2.yCoordinate)], [float(station.xCoordinate), float(station2.xCoordinate)], 'y-')
                           else:
                               plt.plot([float(station.yCoordinate), float(station2.yCoordinate)], [float(station.xCoordinate), float(station2.xCoordinate)], 'y--')

    def new_traject(self, name, station, color):


        # Each new traject has base cost of 20
        self.total_score -= 20

        # Create new traject
        traject = Traject(name, station)

        # Transform string to object
        for row in self.stations:
            if station == row.name:
                start_station = row
                break

        # Travel from start station
        self.travel(traject, start_station, color)
        return traject

    def travel(self, traject, station, color):
        traject_scores = 0

        # Maximum time is 120 mins
        if traject.total_time <= 120:

            # Initialize lists
            possible_names = []
            possible_times = []
            possible_values = []
            possible_scores = []

            # Add relevant connections to relevant lists
            for connection in self.connections:
                if station.name == connection.stationA:
                    possible_names.append(connection.stationB)
                    possible_times.append(connection.travelTime)
                    possible_values.append(connection.critical)
                    possible_scores.append(connection.calc_val())
                elif station.name == connection.stationB:
                    possible_names.append(connection.stationA)
                    possible_times.append(connection.travelTime)
                    possible_values.append(connection.critical)
                    possible_scores.append(connection.calc_val())

            # Looks for best score and according travel time
            best_score = max(possible_scores)
            best_time = possible_times[possible_scores.index(best_score)]


            # If maximum time is not yet exceeded, add fastest connection to traject
            if traject.total_time + best_time <= 120:
                # Add time to traject total time and score to total score
                traject.total_time += best_time
                traject_scores += best_score
                traject.scores.append(traject_scores)

                # Transform string to station
                next_station = self.to_station(possible_names[possible_scores.index(best_score)])

                # Set critical (multiplier) to zero)
                for connection in self.connections:
                    if (station.name == connection.stationA or station.name == connection.stationB) and (next_station.name == connection.stationA or next_station.name == connection.stationB):
                        connection.critical = 0

                # Reset current station and add station to traject list
                traject.traject.append(station.name)
                current_station = next_station

                # Travel again from new station
                self.travel(traject, current_station, color)

            # If travel time exceeds 120 mins
            else:
                # Remove all unneccessary connections
                print("Check")
                self.remove_unnecessary(traject)
                print(traject.traject)
                print(traject.scores)
                print(str(sum(traject.scores)) + "\n")
                return traject
        else:
            # Remove all unneccessary connections
            print("Check")
            self.remove_unnecessary(traject)
            print(traject.traject)
            print(traject.scores)
            print(str(sum(traject.scores)) + "\n")
            return traject

    def all_stations(self, color):
        ## Goes over all start stations and chooses best traject


        # Initialize lists
        trajecten = []
        scores = []

        # Goes over all start stations
        for x in range(len(self.stations)):

            # Reset critical stations
            self.is_critical()

            print(self.stations[x].name)

            # Create new traject and travel
            traject = self.new_traject(str(x), self.stations[x].name, "c")
            trajecten.append(traject)
            scores.append(sum(traject.scores))

        # Choose traject with highest score
        index = scores.index(max(scores))
        best_traject = trajecten[index]

        print(best_traject.traject[0])
        print(best_traject.traject)
        print(sum(best_traject.scores))

        # Plot traject
        self.plot_traject(best_traject, color)

    def plot_traject(self, traject, color):
        ## plots traject once best traject is chosen

        # goes over every station in traject and plots it
        for x in range(1, len(traject.traject)):
            station1 = self.to_station(traject.traject[x-1])
            station2 = self.to_station(traject.traject[x])

            plt.plot([float(station1.yCoordinate), float(station2.yCoordinate)], [float(station1.xCoordinate), float(station2.xCoordinate)], color+"-")


    def remove_unnecessary(self, traject):
        ## Removes all negative scores at the end of the traject

        # Repeats as many times as there are scores
        for x in range(len(traject.scores)):

            # If last element in list is negative, it's an unnecessary connection and neds to be removed
            if traject.scores[-1] < 0:
                traject.scores.pop(-1)
                traject.traject.pop(-1)
            else:
                self.total_score += sum(traject.scores)
                return traject


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
    NH.all_stations("r")
    plt.show()
    print(NH.total_score)
