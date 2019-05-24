# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:34:16 2019

@author: User
"""



# Initial traject object
class Traject(object):
    def __init__(self, start_station):
        self.start_station = start_station
        self.total_time = 0
        self.score = 0
        self.traject = []
        self.scores = []
        self.connections = []
        self.times = []

    def __str__(self):
        return ",".join(self.traject)

    def print_all(self):
        print(self.start_station)
        print(self.total_time)
        print(self.traject)
        print(self.scores)
        print(self.connections)
        print(self.times)
