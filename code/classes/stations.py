# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 21:23:48 2019

@author: User
"""



# Initial staions objects
class Station(object):
    def __init__(self, name, xCoordinate, yCoordinate, critical = False):
        self.name = name
        self.xCoordinate = xCoordinate
        self.yCoordinate = yCoordinate
        self.connectedStations = []

        if critical == "Kritiek":
            self.critical = True
        else:
            self.critical = False

    def __str__(self):
        return self.name
