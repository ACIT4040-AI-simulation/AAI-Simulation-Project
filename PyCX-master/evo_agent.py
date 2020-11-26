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

            
    def getInfectionRate(self):
        return self.infectionRate
            
                    
    

   
# , DONT USE THIS IN PYTEST!!!!!!!!!!!!!!!
def main():

    agenList = json.load(open(os.path.abspath(os.path.dirname(__file__)) + "/agentdata.json"))
    agentObjList = []

    for agentObj in agenList:
        temp = evo_agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'], 0)
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
    