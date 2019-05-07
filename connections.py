# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:07:01 2019

@author: User
"""



# Initial connection objects
class Connection(object):
    def __init__(self, stationA, stationB, travelTime, index, chooseConnection):    #index,
        self.stationA = stationA
        self.stationB = stationB
        self.travelTime = int(travelTime)
        self.chooseConnection = chooseConnection
        self.travelled = False
        self.critical = 1


    def calc_val(self):
        ## Calculates value according to given formula
        score = self.critical * (10000 / 28) - self.travelTime / 10
        return score

    def __str__(self):
        return str(self.stationA + " - " + self.stationB + ": " + str(self.travelTime))
