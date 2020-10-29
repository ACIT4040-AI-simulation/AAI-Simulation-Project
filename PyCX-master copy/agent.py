#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:30:26 2020

@author: kassahundegena
"""

import json
import random
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
# # =============================================================================
# #     #agent actions[   [1,"passing"], 
#                         [2,"cuffing"],
#                         [3,"greeting_by_hand"], 
# #                       [4,"talking_to_one"],
#                         [5,"Talking with group"]]
# =============================================================================
        myaction = random.randint(1,5)
        if myaction ==1:
            pass
        elif myaction == 2:
            for ag in perceptionsList:
                self.will_get_infected(ag)
        elif myaction == 3: 
            ag = random.choice(perceptionsList) 
            self.will_get_infected(ag)

        elif myaction == 4:
            ag = random.choice(perceptionsList) 
            self.will_get_infected(ag)

        elif myaction == 5:
            for ag in perceptionsList:
                self.will_get_infected(ag)
     
        for perception in perceptionsList:
            if isinstance(perception, agent):
                self.perceptAgent(perception)
            else:
                pass
            
    def will_get_infected(self, agent_in):
               
            if (self.status == 'I' and agent_in.status != 'I'):
                prob = self.calcprobablity(self, agent)
                if  random.choice([True, False], 1, p=[prob, 1-prob]):
                    agent_in.status =  'I'
                    agent_in.infect_By = self
                    self.infect_to_List.append(agent_in)
                
            elif(self.status != 'I' and agent_in.status == 'I'):
                prob = self.calcprobablity(self, agent)
                if  random.choice([True, False], 1, p=[prob, 1-prob]):
                    self.status =  'I'
                    self.infect_By = agent_in
                    agent_in.infect_to_List.append(self)
                    
                    
    def perceptObject(self, object):
        #to be coded after we implment classrooms and object classes.
        pass
    
    #aim to determine the agentStatus= from "S" to "I"
    def infected(self,agent):
        self.infected_By = agent
        #agent.infect_to_List.append(self)


    def calcprobablity(self, agent_in)    :
        #mask
        tr = 0
       
        if (self.mask == True and agent_in.mask == True):
            tr = 0.015
        elif ((self.mask == True and agent_in.mask == False) or (self.mask == False and agent_in.mask == True)):
            tr = 0.05
        else:
            tr = 0.70
        
        #Sanitiser
        if (self.antibac >3 and agent_in.antibac >3):
            tr = tr*0.16
        elif (self.antibac >=5 or agent_in.antibac >=5):
            tr = tr*0.16  
        
# =============================================================================
#         #distance
#         distance = sqrt((self.x-agent_in.x)**2 + (self.y-agent_in.y)**2)
# =============================================================================
        if self.distance(self, agent_in) >= s_distance_standard:
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

    for agentObj in agenList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'])
        print(temp.tostring())
        

if __name__ == "__main__":
    main()
    