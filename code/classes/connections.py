# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:07:01 2019

@author: User
"""



# Initial connection objects
class Connection(object):
    def __init__(self, stationA, stationB, travelTime, id = None):    #index,
        self.stationA = stationA
        self.stationB = stationB
        self.travelTime = int(float(travelTime))
        self.travelled = False
        self.critical = 0
        self.id = id


    def calc_val(self, crit_stations):
        ## Calculates value according to given formula
        if self.travelled == False:
            score = self.critical * (10000 / crit_stations) - self.travelTime / 10
        else:
            score = 0 - self.travelTime / 10
        return score

    def __str__(self):
        return str(self.stationA + " - " + self.stationB + ": " + str(self.travelTime))
