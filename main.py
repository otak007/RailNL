import csv
import matplotlib.pyplot as plt


# Initial staions objects
class Station(object):
    def __init__(self, name, xCoordinate, yCoordinate, critical):
        self.name = name
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate

        if critical == "Kritiek":
            self.critical = True

        else:
            self.critical = False

            
# Initial connection objects            
class Connection(object):
    def __init__(self, stationA, stationB, travelTime, chooseConnection):
        self.stationA = stationA
        self.stationB = stationB
        self.travelTime = travelTime
        self.chooseConnection = chooseConnection

       
# Read excel file and create a list with station objects
with open('StationsHolland.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    stations = []

    for row in csv_reader:
        stations.append(Station(row[0], row[1], row[2], row[3]))
        plt.plot(float(row[2]), float(row[1]), "bo")
        plt.text(float(row[2]) -0.02, float(row[1])+0.02, row[0], fontsize=5)

        
    nrOfStations = len(stations)


# Read excel file and create a list with connection objects
with open('ConnectiesHolland.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    connections = []
    for row in csv_reader:
        connections.append(Connection(row[0], row[1], row[2], False))
    nrOfConnections = len(connections)

# Number of choosen connections 
nocc = 0

a=0

# Choose every critical connection
for station in stations:

    if station.critical:
        for connection in connections:
            
            if station.name == connection.stationA and connection.chooseConnection == False: 
               nocc = nocc + 1 
               connection.chooseConnection = True

               for station2 in stations:
                   if station2.name == connection.stationB:
                       plt.plot([float(station.yCoordinate), float(station2.yCoordinate)], [float(station.xCoordinate), float(station2.xCoordinate)], 'r-')


            elif station.name == connection.stationB and connection.chooseConnection == False:
                nocc = nocc + 1
                connection.chooseConnection = True
               
                for station1 in stations:
                   if station1.name == connection.stationA:
                       plt.plot([float(station.yCoordinate), float(station1.yCoordinate)], [float(station.xCoordinate), float(station1.xCoordinate)], 'r-')

            else:
                for station3 in stations:
                    for station4 in stations:
                       if (station3.name == connection.stationA or station3.name == connection.stationB) and (station4.name == connection.stationA or station4.name == connection.stationB) and connection.chooseConnection == False:
                           plt.plot([float(station3.yCoordinate), float(station4.yCoordinate)], [float(station3.xCoordinate), float(station4.xCoordinate)], 'k-')        
                    
print(nocc)
print(nrOfConnections)
plt.show()        
    
        
    
    
    
        
