#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:30:26 2020

@author: kassahundegena
"""

import json
import random
from numpy.random import choice
import itertools  


from math import sqrt

s_distance_standard = 0.01

class agent():
    def __init__(self, id_no, age, sex, status, mask, antibac, socialDistance):
        self.id_no = id_no
        self.age = age
        self.sex = sex
        self.status = status #infected, recoverd, sesuptable, ,
        self.mask = mask
        self.antibac = antibac #rate 1-6
        self.socilDistance = socialDistance # rate setted with local agency
        self.action =''
        self.infected_By = ''
        self.infect_to_List = []
        self.whereAmI = 0
        
    def tostring(self):
        print(self.id_no, 'lala')
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
        myaction = random.randint(1,5)
        if myaction ==1:
            pass
        elif myaction == 2:
            for ag in perceptionsList:
                self.will_get_infected(ag)
        elif myaction == 3: 
            ag = choice(perceptionsList) 
            self.will_get_infected(ag)
        elif myaction == 4:
            ag = choice(perceptionsList) 
            self.will_get_infected(ag)
        elif myaction == 5:
            for ag in perceptionsList:
                self.will_get_infected(ag)
     
            
    def will_get_infected(self, agent_in):
               
            if (self.status == 'I' and agent_in.status != 'I'):
                prob = self.calcprobablity(agent_in)
                if  choice([True, False], 1, p=[prob, 1-prob]):
                    agent_in.status =  'I'
                    print(agent_in.id_no, 'get infected', agent_in.status)
                    agent_in.infect_By = self
                    self.infect_to_List.append(agent_in)
                
            elif(self.status != 'I' and agent_in.status == 'I'):
                prob = self.calcprobablity(agent_in)
                if  choice([True, False], 1, p=[prob, 1-prob]):
                    self.status =  'I'
                    print(agent_in.id_no, 'get infected', agent_in.status)
                    self.infect_By = agent_in
                    agent_in.infect_to_List.append(self)
                    
                    
    def perceptObject(self, object):
        #to be coded after we implment classrooms and object classes.
        pass
    
    #aim to determine the agentStatus= from "S" to "I"
    def infected(self,agent):
        self.infected_By = agent
        #agent.infect_to_List.append(self)


    def calcprobablity(self, agent_in):
        #mask
        tr = 0
       
        if ((self.mask == True) and (agent_in.mask == True)):
            tr = 0.015
        elif ((self.mask == True and agent_in.mask == False) or (self.mask == False and agent_in.mask == True)):
            tr = 0.05
        else:
            tr = 0.70
        
        #Sanitiser antibac
        if ((self.antibac > 3 )and (agent_in.antibac > 3)):
            tr = tr*0.16
        elif ((self.antibac > 5) or (agent_in.antibac > 5)):
            tr = tr*0.16  
        
# =============================================================================
#         #distance
#         distance = sqrt((self.x-agent_in.x)**2 + (self.y-agent_in.y)**2)
# =============================================================================
        if self.distance(agent_in) >= s_distance_standard:
            tr = tr * 0.82
        return tr
# =============================================================================
# To be Done
# We need to consider 2 interactions with: 1.Interaction between the agent and the other agent(s) 
# 					 2.Interaction between the agent and the environment 
#   
# =============================================================================
#for test purposes
def main():

    agenList = json.load(open("agentdata.json"))
    agentObjList = []

    for agentObj in agenList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'])
        temp.x = random.random()
        temp.y = random.random()
        agentObjList.append(temp)
        #print(temp.tostring())
    
    ag = agentObjList[1]
    ag.status = "I"
    ag.mask = False
    
# =============================================================================
#     #testag1 = 
#     ag1 = agentObjList[3]
#     ag2= agentObjList[5]
#     ag3 = agentObjList[10]
#     agentObjList[29].status='I'
#     ag4 = agentObjList[29]
#     ag5 = agentObjList[40]
#     agentObjList[40].status='I'
#     
#     ag6 = agentObjList[22]
# =============================================================================


    neighbors = [nb for nb in agentObjList if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < 0.08**2]
    
    #neighbors = [ag1,ag2,ag3, ag4,ag5,ag6]
    copyneighbors = neighbors.copy()
    for ag1 in neighbors:
         print('Before Agent', ag1.id_no, 'was = ' , ag1.status)
    ag.behavior(neighbors)
    for ag1 in neighbors:
         print('After :Agent', ag1.id_no, 'was = ' , ag1.status)
# =============================================================================
#     for (agNow, agWas) in zip(neighbors,copyneighbors):
#         if agNow.status != agWas.status:
#             pass
#         print('Agent', agWas.id_no, 'was = ' , agWas.status, 'now = ',agNow.id_no, ' =', agNow.status)
#         
# =============================================================================


if __name__ == "__main__":
    main()
    