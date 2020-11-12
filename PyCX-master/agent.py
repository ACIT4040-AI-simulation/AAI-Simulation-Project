#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct 12 21:30:26 2020

@author: kassahundegena
"""

import json
import random

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
        self.classGroup = 1
        
        # print("agents class design is under development")
    
    #testing and debug
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
    def behavior(self,perceptionsList):
    #iterate perseption list
        for perception in perceptionsList:
            if isinstance(perception, agent):
                self.perceptAgent(self,perception)
            else:
                pass
            '''
            agent_action = random(1:5)
            	if agent_state[agent_action]:
            		action = 
            	elif perception == "door":
            		action= "open_door"
            	elif perception == "enter_ corridor":
            		action = "move_to_class"
            	elif perception == "class":
            		action= "open_door"
            	else:
            		action = agent_state
            	return (action)
            '''
    def perceptAgent(self, agent_in):
        #agent_actions = [[1,"passing"], [2,"cuffing"],[3,"greeting_by_hand"], [4,"talking_to"],[5,"moving_class"]]
        myaction = random(1,5)  
        agent_action = random(1,5) 
        if myaction == 1:
            pass
        elif myaction == 2:
            pass 
            ''' if both caff, one cuff, 
            lets have data about the probablity(data collection) and matrix from test teams
            '''
        elif myaction == 3:
            # xOr =  (a and not b) or (not a and b)
            '''assume hanshake is 70% transmission rate
                if mask the risk will half
                if sanitise  25% less
                then we have to get probablity( from data collection) and matrix from test teams
                change_status
                '''
                #calcprobablity(self, agent)
            if (self.status == 'I' and agent_in.status != 'I'):
                #calcprobablity(self, agent)
                prob = 0.9
                if prob > 0.75:
                    agent_in.status =  'I'
                
                pass
            elif(self.status != 'I' and agent_in.status == 'I'):
                #if my probablitiy gigevs me infected
                self.infected(agent)

        elif myaction == 4: 
            pass
        elif myaction == 5:
            pass
        elif myaction == 6:
            pass
                    
    def perceptObject(self, object):
        #to be coded after we implment classrooms and object classes.
        pass
    
    #aim to determine the agentStatus= from "S" to "I"
    def infected(self,agent):
        self.infected_By = agent
        #agent.infect_to_List.append(self)

'''
We need to consider 2 interactions with: 1.Interaction between the agent and the other agent(s) 
					 2.Interaction between the agent and the environment 
'''   
#for test purposes
def main():

    agenList = json.load(open("agentdata.json"))

    for agentObj in agenList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'])
        print(temp.tostring())
        
    
        

if __name__ == "__main__":
    main()
    