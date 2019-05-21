from connectionsSander import Connection
from stations import Station
from trajectSander import Traject

import csv
import matplotlib.pyplot as plt

class Map(object):

    def __init__(self):
        self.connections = self.load_connections()
        self.stations = self.load_stations()
        self.total_score = 0
        self.trajecten = []
        self.scores = []
        self.driven_connections = []

    def load_connections(self):
        # Read excel file and create a list with connection objects
        with open('data/ConnectiesNationaal.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            connections = []
            for row in csv_reader:
                connections.append(Connection(csv_reader.line_num, row[0], row[1], row[2]))
            return connections

    def load_stations(self):
        # Read excel file and create a list with station objects
        with open('data/StationsNationaal.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            stations = []

            for row in csv_reader:
                stations.append(Station(row[0], row[1], row[2], row[3]))
                plt.plot(float(row[2]), float(row[1]), "bo")
                plt.text(float(row[2]) -0.02, float(row[1])+0.02, row[0], fontsize=5)
            return stations

    def is_critical(self):

        crit_stations = []

        # Checks if connection is connected to critical station
        for station in self.stations:
            for connection in self.connections:
                if self.driven_connections:
                    if connection not in self.driven_connections:
                        connection.critical = 1
                    else:
                        connection.critical = 0
                else:
                    connection.critical = 1
                    crit_stations.append(connection)

    def plot(self):

        for station in self.stations:

            for connection in self.connections:

                if station.name == connection.stationA or station.name == connection.stationB:

                   for station2 in self.stations:
                       if station2.name == connection.stationB or station2.name == connection.stationA:
                           if station.critical or station2.critical:
                               plt.plot([float(station.yCoordinate), float(station2.yCoordinate)], [float(station.xCoordinate), float(station2.xCoordinate)], 'y-')
                           else:
                               plt.plot([float(station.yCoordinate), float(station2.yCoordinate)], [float(station.xCoordinate), float(station2.xCoordinate)], 'y-')

    def new_traject(self, station, color):

        # Create new traject
        traject = Traject(station)

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

        # Initialize lists
        possible_names = []
        possible_times = []
        possible_scores = []
        possible_connections = []

        # Add relevant connections to relevant lists
        for connection in self.connections:
            if station.name == connection.stationA:
                possible_connections.append(connection)
                possible_names.append(connection.stationB)
                possible_times.append(connection.travelTime)
                possible_scores.append(connection.calc_val())
            elif station.name == connection.stationB:
                possible_connections.append(connection)
                possible_names.append(connection.stationA)
                possible_times.append(connection.travelTime)
                possible_scores.append(connection.calc_val())
        print(possible_names)
        print(possible_scores)
        print("\n")
        # Looks for best score and according travel time
        best_score = max(possible_scores)
        best_time = possible_times[possible_scores.index(best_score)]

        # If maximum time is not yet exceeded, add fastest connection to traject
        if traject.total_time + best_time <= 180:

            # Add time to traject total time and score to total score
            traject.total_time += best_time
            traject_scores += best_score
            traject.scores.append(traject_scores)

            # Transform string to station
            index = possible_scores.index(best_score)
            chosen_connection = possible_connections[index]
            next_station = self.to_station(possible_names[index])

            # Set critical (multiplier) to zero)
            for connection in self.connections:
                if (connection == chosen_connection):
                    connection.critical = 0

            # Reset current station and add station to traject list
            traject.connections.append(chosen_connection)
            if not traject.traject:
                traject.traject.append(station.name)
            traject.traject.append(next_station.name)

            # Travel again from new station
            self.travel(traject, next_station, color)

        # If travel time exceeds 120 mins
        else:
            # Remove all unneccessary connections
            self.remove_unnecessary(traject)
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


            # Create new traject and travel
            traject = self.new_traject(self.stations[x].name, "c")
            trajecten.append(traject)
            scores.append(sum(traject.scores))

        # Choose traject with highest score
        index = scores.index(max(scores))
        best_traject = trajecten[index]

        # add connections from best traject to list of already driven connections
        self.driven_connections.extend(best_traject.connections)
        self.driven_connections = list(dict.fromkeys(self.driven_connections))

        # add score to total score, subtract 20 as base cost
        self.total_score += sum(best_traject.scores) - 20

        self.scores.append(sum(best_traject.scores))
        self.trajecten.append(best_traject)
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
        counter = 0
        # Repeats as many times as there are scores
        for x in range(1,len(traject.scores)):

            # If last element in list is negative, it's an unnecessary connection and neds to be removed
            if traject.scores[-1] < 0:
                counter += 1
                traject.scores.pop(-1)
            else:
                return traject

        del traject.traject[-counter:]
        del traject.connections[-counter:]

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
    NH.all_stations("b")
    NH.all_stations("r")
    NH.all_stations("c")
    NH.all_stations("k")
    NH.all_stations("g")
    NH.all_stations("r")
    NH.all_stations("b")
    NH.all_stations("r")
    NH.all_stations("g")
    NH.all_stations("k")
    NH.all_stations("c")
    NH.all_stations("r")
    NH.all_stations("g")
    NH.all_stations("k")
    NH.all_stations("r")
    print(NH.total_score)
    plt.show()
