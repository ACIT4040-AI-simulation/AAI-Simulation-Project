# -*- coding: utf-8 -*-
"""
Created on Sat Nov  7 15:01:47 2020
@author: fatem
"""

import numpy as np
import random
from heapq import nsmallest

optimal_solution=[]

def random_array_generator():
    random_float_array = np.random.uniform(0, 1.0, size=(10, 3))
    random_generator=np.around(random_float_array,2)
    random_generator=random_generator.tolist()
    for i in random_generator :
        i.append((random.randint(50,200)))
    
    random_generator=np.array(random_generator)
    
    #print(random_generator)
    return random_generator

def sorted_population(random_generator): #it will return the random nos who are in the cost budget
    #arr=random_array_generator()
    #print(random_generator, "inside sorted")
    Mask_cost=0.5
    HS_cost=0.3
    SD_cost=0.6
    costs= np.array([Mask_cost, HS_cost, SD_cost])
    sorted_pop=[]
    sorted_pop_final=[]
    PopulationNumberArray = []
    for i in random_generator:
        arr_cost=np.around(i[0:3]*costs, 2)
        sum_cost=np.sum(arr_cost)
        #print(sum_cost)
    
        if sum_cost<=0.80:
           sorted_pop=np.append([sorted_pop],[i])
           PopulationNumberArray.append(i[3])
           #print(type(sorted_pop)),

    sorted_pop = sorted_pop.reshape(-1,4)#gives an array of measures which are in the budget
    
    sorted_pop_list= sorted_pop.tolist()
    
    for i in sorted_pop_list:
        if i[3]<=180 and i[3]>=70:
           sorted_pop_final.append(i)
        
    print("check",sorted_pop_final)
    sorted_population_final= np.array(sorted_pop_final)
    #print np.array_str(sorted_population_final, precision=2, suppress_small=True)
           
    return sorted_population_final

def fitness_score(sorted_arr, Infection_rate):
   lowest_two_infections = nsmallest(2, Infection_rate)
   print(lowest_two_infections, "2 lowest rates")
   lowest_infection_rate = lowest_two_infections[0]
   lowest_index = Infection_rate.index(lowest_infection_rate)
   parent1 = sorted_arr[lowest_index]
   
   second_lowest_infection_rate = lowest_two_infections[1]
   second_lowest_index = Infection_rate.index(second_lowest_infection_rate)
   #parent1 = random_arr[lowest_index]
   parent2 =  sorted_arr[second_lowest_index]
   parent1_IR= np.append(parent1, lowest_infection_rate )
   parent2_IR= np.append(parent2, second_lowest_infection_rate )
   #print("Lowest infection value:", lowest_infection_rate) 
   #print("Second_Lowest infection value:", second_lowest_infection_rate)
   print ("Parent1: ")
   print (np.array_str(parent1_IR, precision=2, suppress_small=True))
   print ("Parent2: ")
   print (np.array_str(parent2_IR, precision=2, suppress_small=True))
   return parent1_IR, parent2_IR

def selectOptimalSolution(parents):
    parents=np.array(parents)    
    min_infection_parent=parents[parents[:,4].argsort()]
    min_infection_parent= min_infection_parent[0:1, :]
    min_infection_parent= min_infection_parent[0].tolist()
    if len(optimal_solution) == 0:
        optimal_solution.append(min_infection_parent)
    else:
        if optimal_solution[0][4] > min_infection_parent[4]:
            optimal_solution.pop()
            optimal_solution.append(min_infection_parent)
    print ("The optimal Solution is:" ,optimal_solution)
    return optimal_solution

    
def crossover(parents):
    parents=np.array(parents)
    parents = np.delete(parents, 4, axis=1)
    #print(parents)
    
    split=1
    parent1_old= parents[:split,:] # making the 2d array to 2 1d array
    parent2_old =parents[split:,:]
    for i in parent1_old:
        parent1= np.array(i)
    for i in parent2_old:
        parent2= np.array(i)
    
    
    offsprings=[]
    x = 2
    y = 1
    z = 3
    k = 4 # the parents will come
     
  
    offspring_1=np.append(parent1[:x], parent2[x:])
    offspring_2=np.append(parent2[:x], parent1[x:])
    offspring_3=np.append(parent1[:y], parent2[y:])
    offspring_4=np.append(parent2[:y], parent1[y:])
    offspring_5=np.append(parent1[:z], parent2[z:])
    offspring_6=np.append(parent2[:z], parent1[z:])
    offspring_7=np.append(parent1[:k], parent2[k:])
    offspring_8=np.append(parent2[:k], parent1[k:])
    offsprings=np.append(offsprings, [offspring_1,offspring_2,offspring_3,offspring_4,offspring_5,offspring_6,offspring_7,offspring_8])
    offsprings = offsprings.reshape(-1,4)
    print ("After crossover: ")
    print (np.array_str(offsprings, precision=2, suppress_small=True))
    return offsprings

def mutation(mutated_offsprings):# does swaping within 1st and 3rd column also randomly changes the last column which is agents within the range 20 to 180
    start_index = 0 # swaping points
    last_index = 2
    mutated_offsprings [:, [start_index, last_index]] = mutated_offsprings[:, [last_index, start_index]] 
    #print np.array_str(mutated_offsprings, precision=2, suppress_small=True)
    for i in mutated_offsprings:
        i[3]= (random.randint(20,180))
    print ("After mutation: It is swaping betn the 1st&3rd column and changing the last column")
    print (np.array_str(mutated_offsprings, precision=2, suppress_small=True))
    return mutated_offsprings

random_arr= random_array_generator()
sorted_arr=sorted_population(random_arr)