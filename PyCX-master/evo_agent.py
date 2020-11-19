#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:30:26 2020

@author: kassahundegena
"""

import json
import os
import random
from numpy.random import choice
import itertools  

from math import sqrt
s_distance_standard = 0.004

class evo_agent():
    def __init__(self, id_no, age, sex, status, mask, antibac, socialDistance, infectionRate):
        self.id_no = id_no
        self.status = status #infected, recoverd, sesuptable, ,
        self.mask = mask
        self.antibac = antibac
        self.socilDistance = socialDistance # rate setted with local agency
        self.age = age,
        self.sex = sex,
        self.classGroup = 1
        self.infectionRate = infectionRate
        
    def tostring(self):
        print(self.id_no)
        print(self.age)
        print(self.sex)
        print(self.status)
        print(self.mask)
        print(self.antibac)
        print(self.socilDistance)
        print("----------------------------")
        
    #perceptionsList is a list of objects around (object, agent, .....
    # )
    def distance(self, agent_in):
        return sqrt((self.x-agent_in.x)**2 + (self.y-agent_in.y)**2)
    
    def behavior(self,perceptionsList):
# =============================================================================
#       #agent actions[   [1,"passing"], 
#                         [2,"cuffing"],
#                         [3,"greeting_by_hand"], 
#                         [4,"talking_to_one"],
#                         [5,"Talking with group"]]
#
# =============================================================================
        myaction = random.randint(1,2)
        print(myaction)
        if myaction == 1:
            pass
        else:
            self.startInfecting(perceptionsList[0], perceptionsList[1])
            for ag in perceptionsList:
                self.will_get_infected(ag)
            
       

    def startInfecting(self, agent1, agent2):
        if agent1.status == 'S':
            if agent1.status == 'S' and agent2.status == 'I':
                self.calcInfectionRate(agent1, agent2)
            if agent1.infectionRate > random.random():
                agent2.status = 'I'
                agent2.infectionRate =0
                    
        elif agent1.status == 'I':
            if random.random() < 0.4 :
                agent2.status = 'R'
            
            if agent2.status == 'S':
                self.calcInfectionRate(agent1, agent2)
                #decide wether if greater than or less than 
            if agent1.infectionRate > random.random():
                agent2.status = 'I'
                agent2.infectionRate = 0

    def calcInfectionRate(self, currentNode, neighbourNode):
        infectionRateList=[]
    #if the current node infected and the neighbour is susceptible
        if (currentNode.status == 'I'):
            if (currentNode.mask == True):
                if (neighbourNode.mask == True):
                    neighbourNode.infectionRate = 0.015
                elif (neighbourNode.mask != True):
                    neighbourNode.infectionRate = 0.05
            elif currentNode.mask != True:
                neighbourNode.infectionRate = 0.7
            
            #check if the current node applying HandSani
            if neighbourNode.antibac == True:
                neighbourNode.infectionRate = neighbourNode.infectionRate * 0.16
            
            #check if the neighbour node applying socialDistance
            if neighbourNode.socilDistance == True:
                neighbourNode.infectionRate = neighbourNode.infectionRate * 0.40
                            
            if neighbourNode.infectionRate>0:
                infectionRateList.append(neighbourNode.infectionRate)
            
        #if the current node susceptible and the neighbour is infected    
        elif currentNode.status == 'S':
            if neighbourNode.mask == True:
                if currentNode.mask == True:
                    currentNode.infectionRate = 0.015
                elif currentNode.mask != True:
                    currentNode.infectionRate = 0.05
            elif neighbourNode.mask != True:
                currentNode.infectionRate = 0.7
            
            #check if the current node applying HandSani
            if currentNode.antibac == True:
                currentNode.infectionRate = currentNode.infectionRate * 0.16
            
            #check if the current node applying socialDistance
            if currentNode.socilDistance:
                currentNode.infectionRate = currentNode.infectionRate * 0.40            
            
            if currentNode.infectionRate>0:
                infectionRateList.append(currentNode.infectionRate)
            print(infectionRateList)

            
        def will_get_infected(self, agent_in):
            if ((self.status == 'I' or self.status == 'R') and agent_in.status != 'I'):
                prob = self.calcprobablity(agent_in)
                if  choice([True, False], 1, p=[prob, 1-prob]):
                    agent_in.status =  'I'
                    agent_in.infclock = self.clock
                    agent_in.inf_counter +=1
                    print(agent_in.id_no, 'get infected', agent_in.status)
                    agent_in.infect_By = self
                    self.infect_to_List.append(agent_in)
                
            elif(self.status != 'I' and (agent_in.status == 'I' or agent_in.status == 'R')):
                prob = self.calcprobablity(agent_in)
                if  choice([True, False], 1, p=[prob, 1-prob]):
                    self.status =  'I'
                    self.infclock = self.clock
                    self.inf_counter +=1 
                    #print(agent_in.id_no, 'get infected', agent_in.status)
                    self.infect_By = agent_in
                    agent_in.infect_to_List.append(self)
                    
    

    def calcprobablity(self, agent_in):
        #mask
        tr = 0
        if ((self.mask == True) and (agent_in.mask == True)):
            tr = 0.1
        elif ((self.mask == True and agent_in.mask == False) or (self.mask == False and agent_in.mask == True)):
            tr = 0.4
        else:
            tr = 0.70
        
        #Sanitiser antibac
        if ((self.antibac == True ) and (agent_in.antibac == True)):
            tr = tr*0.36
        elif (self.antibac != agent_in.antibac ):
            tr = tr*0.18         
# =============================================================================
#         #distance
#         distance = sqrt((self.x-agent_in.x)**2 + (self.y-agent_in.y)**2)
# =============================================================================
        if self.distance(agent_in) >= s_distance_standard:
            tr = tr * 0.82
        return tr

#for test purposes
def main():

    agenList = json.load(open(os.path.abspath(os.path.dirname(__file__)) + "/agentdata.json"))
    agentObjList = []

    for agentObj in agenList:
        temp = evo_agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'])
        temp.x = random.random()
        temp.y = random.random()
        agentObjList.append(temp)
        #print(temp.tostring())
    
    ag = agentObjList[1]
    ag.status = "I"
    ag.mask = False

    neighbors = [nb for nb in agentObjList if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < 0.08**2]
    copyneighbors = neighbors.copy()
    for ag1 in neighbors:
         print('Before Agent', ag1.id_no, 'was = ' , ag1.status)
    ag.behavior(neighbors)
    for ag1 in neighbors:
         print('After :Agent', ag1.id_no, 'was = ' , ag1.status)

if __name__ == "__main__":
    main()
    