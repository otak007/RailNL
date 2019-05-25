from code.classes.connections import *
from code.classes.stations import *

import csv
import matplotlib.pyplot as plt


class Map(object):

    def __init__(self, data, crit):
        self.data = data
        self.stations = self.load_stations(crit)
        self.connections = self.load_connections(crit)
        self.total_score = 0
        self.trajecten = []
        self.scores = []
        self.driven_connections = []

    def load_connections(self, crit):
        # Read excel file and create a list with connection objects
        with open('data/Connecties'+self.data+'.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            connections = []
            for row in csv_reader:
                connections.append(Connection(row[0], row[1], row[2], csv_reader.line_num))
                for station in self.stations:
                    for station2 in self.stations:
                        if (station.name == row[1] and station2.name == row[0]) or (station.name == row[0] and station2.name == row[1]):
                            if crit == "yes" or (station.critical == True or station2.critical == True):
                                plt.plot([float(station.yCoordinate), float(station2.yCoordinate)], [float(station.xCoordinate), float(station2.xCoordinate)], 'y-')
                            else:
                                plt.plot([float(station.yCoordinate), float(station2.yCoordinate)], [float(station.xCoordinate), float(station2.xCoordinate)], 'y:')
            return connections

    def load_stations(self, crit):
        # Read excel file and create a list with station objects
        with open('data/Stations'+self.data+'.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')

            stations = []

            for row in csv_reader:
                stations.append(Station(row[0], row[1], row[2], row[3]))
                if row[3] == "Kritiek" or crit == "yes":
                    plt.plot(float(row[2]), float(row[1]), "ro")
                else:
                    plt.plot(float(row[2]), float(row[1]), "bo")
                plt.text(float(row[2]) -0.02, float(row[1])+0.02, row[0], fontsize=5)
            return stations
