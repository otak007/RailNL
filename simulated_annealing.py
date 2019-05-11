from connections import Connection
from stations import Station
from traject import Traject
from main import map

import csv
import matplotlib.pyplot as plt

# Simulated Annealing SA
def SA(problem, iter, temp_max)
    Solution_current = Calculate_Solution(problem)
    Solution_best = Solution_current

    for i in range(iter)
        S_i = Calculate_K_NeighbourSolution(Solution_current)
        temp_currunt = CalculateTemp(i, temp_max)

        if (Calculate_K(S_i) =< Calculate_K(Solution_current))
            Solution_current = S_i
            if (Calculate_K(S_i) =< Calculate_K(Solution_best))
                Solution_best = S_i

        elif ( exp(Calculate_K(Solution_current)-Calculate_K(S_i))/temp_currunt > random(0,1))
            Solution_current = S_i


return S_best
