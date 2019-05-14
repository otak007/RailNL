from connections import Connection
from stations import Station
from traject import Traject

import random
import csv
import matplotlib.pyplot as plt
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
                plt.plot(float(row[2]), float(row[1]), "bo")
                plt.text(float(row[2]) -0.02, float(row[1])+0.02, row[0], fontsize=5)
            return stations
    
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
                        
    # Create a traject with a random begin station
    def random_traject(self):
        trajecten = []
        for x in range(500):
            index = random.randint(0, len(self.stations) - 1)
            begin_station = self.stations[index].name
            trajecten.append(self.new_traject(str(x), begin_station, "c"))

    # Create a new traject    
    def new_traject(self, name, station, color):
        traject = Traject(name, station)
        for row in self.stations:
            if station == row.name:
                start_station = row
                break
        self.travel(traject, start_station, color)



    def travel(self, traject, station, color):
        # Initialize lists
        possible_connections = []
        possible_names = []
        possible_times = []


        # Maximum time is 120 mins
        if traject.total_time < 120:
            
            # Add relevant connections to relevant lists
            for connection in self.connections:
                if station.name == connection.stationA and connection.travelTime + traject.total_time < 120:
                    possible_names.append(connection.stationB)
                    possible_times.append(connection.travelTime)
                    possible_connections.append(connection)

                elif station.name == connection.stationB and connection.travelTime + traject.total_time < 120:
                    possible_names.append(connection.stationA)
                    possible_times.append(connection.travelTime)
                    possible_connections.append(connection)
            
            # return the traject when no other connection is possible to add to the traject
            if len(possible_connections) == 0:
                print(traject.traject)
                return traject.traject

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
                    
            current_station = next_station
               

            # Travel again with 
            self.travel(traject, current_station, color)                

                        
                               
                               
if __name__ == "__main__":
    NH = Map()
    start = time.time()  
    NH.random_traject()
    end = time.time()
    print(end-start)
    NH.load_connections()



    
