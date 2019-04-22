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

    def travel(self, traject, station, color):
        traject_scores = 0

        # Maximum time is 120 mins
        if traject.total_time < 120:

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
                next_station = possible_names[possible_times.index(best_time)]
                for row in self.stations:
                    if next_station == row.name:
                        next_station = row
                        break


                # Set critical (multiplier) to zero)
                for connection in self.connections:
                    if (station.name == connection.stationA or station.name == connection.stationB) and (next_station.name == connection.stationA or next_station.name == connection.stationB):
                        connection.critical = 0

                # Reset current station
                traject.traject.append(station.name)

                current_station = next_station
                plt.plot([float(station.yCoordinate), float(next_station.yCoordinate)], [float(station.xCoordinate), float(next_station.xCoordinate)], color+"-")


                # Travel again from new station
                self.travel(traject, current_station, color)

            # If travel time exceeds 120 mins
            else:
                # Remove all unneccessary connections
                self.remove_unneccessary(traject.scores)
                print(traject.traject)

    def remove_unneccessary(self, scores):
        # Removes all negative scores at the end of the traject
        for x in range(len(scores)):
            if scores[-1] < 0:
                scores.pop(-1)
            else:
                break
        print(sum(scores))
        self.total_score += sum(scores)



if __name__ == "__main__":
    # Initialize map, plot and give four starting stations
    NH = Map()
    NH.plot()
    NH.new_traject("1", "Den Helder", "c")
    NH.new_traject("2", "Dordrecht", "k")
    NH.new_traject("3", "Alkmaar", "b")
    NH.new_traject("4", "Gouda", "r")
    plt.show()
    print(NH.total_score)
