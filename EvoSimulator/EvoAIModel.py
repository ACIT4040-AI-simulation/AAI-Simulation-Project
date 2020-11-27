#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 13:34:11 2020

@author: emanazab
"""

import EvoSimulator.WithoutPyCx as sim
import EvoSimulator.Evopart as evo

new_mutated_offspring =[]
population = evo.random_array_generator()
optimized_solution = None
generation_counter = 0

def getFinalSolution(selected_population):
    global optimized_solution
    try:
        filtered_individuals=evo.sorted_population(selected_population)
        if(len(filtered_individuals) > 2):
            totalInfectionRate= sim.getInfectionRate_ABM(filtered_individuals)
            selected_parents= evo.fitness_score(filtered_individuals,totalInfectionRate)
            print(selected_parents)
            offsprings =evo.crossover(selected_parents)
            mutated_offspring = evo.mutation(offsprings)
            optimized_solution= evo.selectOptimalSolution(selected_parents)
            return mutated_offspring
    except TypeError as e:
        pass
    

    #print(filtered_individuals, "filtered")
    pass

for i in range(500):
    generation_counter += 1
    if i == 0:
        new_mutated_offspring= getFinalSolution(population)
    else:
        new_mutated_offspring= getFinalSolution(new_mutated_offspring)

print(generation_counter, "THE GENERATION COUNTER \n")

print('optimal solution is:','\n',
      'Mask_prob:',optimized_solution[0][0],'\n',
      'HS_prob:',optimized_solution[0][1],'\n',
      'SD_prob:', optimized_solution[0][2],'\n',
      'Population:', optimized_solution[0][3], '\n',
      'Total Infection Rate:', optimized_solution[0][4])
