from connections import Connection
from stations import Station
from traject import Traject
import csv
import matplotlib.pyplot as plt
        
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
                        
    def new_traject(self, name, station, color):
        
        for connection in self.connections:
            connection.travelled == False
            
        traject = Traject(name, station)
        for row in self.stations:
            if station == row.name:
                start_station = row
                break
        self.travel(traject, start_station, color)
        
    def travel(self, traject, station, color):
        
        # Maximum time is 120 mins
        if traject.total_time < 120:
            
            # Initialize lists
            possible_connections = []
            possible_names = []
            possible_times = []
            
            # Add relevant connections to relevant lists
            for connection in self.connections:
                if connection.travelled == False:
                    if station.name == connection.stationA:
                        possible_names.append(connection.stationB)
                        possible_times.append(connection.travelTime)
                        possible_connections.append(connection)
                    elif station.name == connection.stationB:
                        possible_names.append(connection.stationA)
                        possible_times.append(connection.travelTime)
                        possible_connections.append(connection)
            
            
            # Check which station is closest, error here
            if possible_times:
                closest_distance = min(possible_times)
                
                # If maximum time is not yet exceeded, add fastest connection to traject
                if traject.total_time + closest_distance < 120:
                    traject.total_time += closest_distance
                    
                    next_station = possible_names[possible_times.index(closest_distance)]
                    for row in self.stations:
                        if next_station == row.name:
                            next_station = row
                            break
                    
        
                    # Set travelled to true and plot 
                    for connection in self.connections:
                        if (station.name == connection.stationA or station.name == connection.stationB) and (next_station.name == connection.stationA or next_station.name == connection.stationB):
                            connection.travelled = True
                    
                    # Reset current station
                    traject.traject.append(station.name)
                    
                    current_station = next_station
                    plt.plot([float(station.yCoordinate), float(next_station.yCoordinate)], [float(station.xCoordinate), float(next_station.xCoordinate)], color+"-")

    
                    # Travel again with 
                    self.travel(traject, current_station, color)
                else:
                    return traject.traject

            
            
                        
                               
                               
if __name__ == "__main__":
    NH = Map()
    NH.plot()
    NH.new_traject("first", "Den Helder", "c")
    NH.new_traject("second", "Dordrecht", "r")

    