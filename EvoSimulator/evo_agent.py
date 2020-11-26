#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:30:26 2020

@author: kassahundegena 
"""

import random


class evo_agent:
    def __init__(self, id_no, age, sex, status, mask, antibac, socialDistance, infectionRate):
        self.id_no = id_no
        self.status = status
        self.mask = mask
        self.antibac = antibac
        self.socalDistance = socialDistance # rate setted with local agency
        self.age = age,
        self.sex = sex,
        self.classGroup = 1
        self.infectionRate = infectionRate
        
   
    def startInfecting(self, agent1, agent2):
        if agent1.status == 'S':
            if agent1.status == 'S' and agent2.status == 'I':
                self.calcInfectionRate(agent1, agent2)
                if agent1.infectionRate > random.random():
                    agent2.status = 'I'
                    agent2.infectionRate = 0
                    
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
        infectionRateList = []
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
            if neighbourNode.socalDistance == True:
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
            if currentNode.socalDistance:
                currentNode.infectionRate = currentNode.infectionRate * 0.40            
            
            if currentNode.infectionRate > 0:
                infectionRateList.append(currentNode.infectionRate)

            
    def getInfectionRate(self):
        return self.infectionRate

    