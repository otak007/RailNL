from connections import Connection
from stations import Station
from traject import Traject
from collections import deque, namedtuple

import random
import csv
import matplotlib.pyplot as plt
import time
import numpy as np

class Map(object):


    def __init__(self):
        self.connections = self.load_connections()
        self.stations = self.load_stations()


    # de connecties laden en definieren
    def load_connections(self):
        # Read excel file and create a list with connection objects
        with open('ConnectiesHolland.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            index=0
            connections = []
            for row in csv_reader:
                connections.append(Connection(row[0], row[1], row[2], index, False))
                index += 1
            return connections

    # de stations laden en defineren
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

    # een class voor het plotten van degrafiek
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


    # class voor een nieuw traject
    def new_traject(self, name, station):
        traject = Traject(name, station)
        for row in self.stations:
            if station == row.name:
                start_station = row
                break
        self.travel(traject, start_station)

    def dijk_lijst(self):
        a = len(self.stations)
        t=newTable(a,3)
        for station in self.stations:
            t[station, 1] = station.name
            t[station, 3] = 9999999
        return t


    def dijk(self, strt_station):
        start = start_station
        #self.eind_station = eind_station
        bezochte_stations = []
        nietbezochte_stations = []

        # maak een lijstje met nietbezochte stations
        for station in self.stations:
            nietbezochte_stations[station]= stations.name

        # maak een tabel die de kortste route bij houdt
        tabel = dijk_lijst()

        # zet de waarde van het start station op afstand 0
        for station in tabel:
            if tabel[station,1] == start:
                tabel[station,3]=0

        # ga kijken naar de buren van het station
        

        return tabel




if __name__ == "__main__":
    # Initialize map, plot and give four starting stations
    NH = Map()
    #NH.dijk(Alkmaar)
    a = len(NH.stations)
    print(a)
    #NH.dijk(Alkmaar)
