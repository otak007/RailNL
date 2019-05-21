# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:34:16 2019

@author: User
"""



# Initial traject object
class Traject(object):
    def __init__(self, start_station):
        self.start_station = start_station
        self.times = []
        self.traject = []
        self.scores = []
        self.connections = []
        self.score = 0
        self.total_time = 0

    def __str__(self):
        return str(self.traject)
