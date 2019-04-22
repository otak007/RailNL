# -*- coding: utf-8 -*-
"""
Created on Mon Apr  8 22:34:16 2019

@author: User
"""



# Initial traject object
class Traject(object):
    def __init__(self, name, start_station):
        self.name = name
        self.start_station = start_station
        self.total_time = 0
        self.traject = []
        self.scores = []
