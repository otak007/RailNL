# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:07:01 2019

@author: User
"""



# Initial connection objects
class Connection(object):
    def __init__(self, id, stationA, stationB, travelTime):
        self.id = id
        self.stationA = stationA
        self.stationB = stationB
        self.travelTime = int(travelTime)
        self.travelled = False
        self.critical = 0


    def calc_val(self):
        ## Calculates value according to given formula
        if self.travelled is False:
            score = self.critical * (10000 / 28) - self.travelTime / 10
        else:
            score = 0 - self.travelTime / 10
        return score

    def __str__(self):
        return str(self.stationA + " - " + self.stationB + ": " + str(self.travelTime))
