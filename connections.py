# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:07:01 2019

@author: User
"""



# Initial connection objects
class Connection(object):
    def __init__(self, stationA, stationB, travelTime, chooseConnection):
        self.stationA = stationA
        self.stationB = stationB
        self.travelTime = int(travelTime)
        self.chooseConnection = chooseConnection
        self.travelled = False
        self.critical = False
        self.value = 0