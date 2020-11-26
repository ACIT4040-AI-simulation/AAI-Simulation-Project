# -*- coding: utf-8 -*-
"""
Created on Sun Nov  22 23:30:47 2020

@author: Ilham Jilani
"""
from .evo_agent import evo_agent as agent
from PIL import Image as img
import json
import random
import numpy as np
import os

json_agent_filepath = "EvoSimulator/100_Agents.json"
imgPath = os.path.abspath(os.path.dirname(__file__)) + "\\p35-4thfloor_withdoors.png"
im = img.open(imgPath)

DOOR_COLOR = im.getpixel((985, 622))
FLOOR_COLOR = im.getpixel((1113, 329))
NUANCE_COLOR = (215, 201, 198, 255)

validColorZones = [ DOOR_COLOR, FLOOR_COLOR, NUANCE_COLOR]




"""
This will change the percentage of Infected agents according the Initial agentsList
"""
def changePercentageOfInfectedAgents(infectedPercentage, agentsList):
    numberOfAgents = len(agentsList) * infectedPercentage
    agentList = random.sample(agentsList, round(numberOfAgents))
    for i in agentList:
        i.status = 'I'

    return agentsList

"""
This will change the percentage of Infected agents according the Initial agentsList
"""
def changePercentageOfMaskUsers(maskPercentage, agentsList):
    numberOfAgents = len(agentsList) * maskPercentage
    agentList = random.sample(agentsList, round(numberOfAgents))
    for i in agentList:
        i.mask = True    
    
    return agentsList

"""
This will change the percentage of Infected agents according the Initial agentsList
"""
def changePercentageOfSanitizerUsers(sanitizerPercentage, agentsList):
    numberOfAgents = len(agentsList) * sanitizerPercentage
    agentList = random.sample(agentsList, round(numberOfAgents))
    for i in agentList:
        i.antibac = True
    
    return agentsList

    
def upload_agents_json(fileName, infRate, maskRate, sanitizerRate, initPop):
    counter = 0
    jsonAgentList = json.load(open(fileName))
    agentObjList = []

    for agentObj in jsonAgentList:
        counter += 1
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'], agentObj['infectionRate'])
        agentObjList.append(temp)
        if(counter == initPop):
            break

    agentObjList = changePercentageOfInfectedAgents(infRate, agentObjList)
    agentObjList = changePercentageOfMaskUsers(maskRate, agentObjList)
    agentObjList = changePercentageOfSanitizerUsers(sanitizerRate, agentObjList)

    return agentObjList

 
"""
 This will have 4 parameters distance (float), mask (float), sanitizer (float), initial population (INT)

"""
def initializeAgents(infRate, maskRate, sanitizerRate, initPop):
    agentsList = upload_agents_json(json_agent_filepath, infRate, maskRate, sanitizerRate, initPop)
    for ag in agentsList:
        ag.classGroup = random.randint(1,3)
        ag.x = random.randint(600,1800)
        ag.y = random.randint(300,1200)
        pixelColor = im.getpixel((ag.x, ag.y))
        if(pixelColor not in validColorZones):
            randomPlacement = random.randint(1,4)
            if(randomPlacement == 1):
                ag.x = random.randint(360,800)
                ag.y = random.randint(900, 1050)
            if(randomPlacement == 2):
                ag.x = random.randint(2026,2160)
                ag.y = random.randint(921,1129)
            if(randomPlacement == 3):
                ag.x = random.randint(200,500)
                ag.y = random.randint(1180,1300)
            if(randomPlacement == 4):
                ag.x = random.randint(1300, 1400)
                ag.y = random.randint(126,306)
                               
    return agentsList


def observe():
    global agentsList

    infected = [ag for ag in agentsList if ag.status == 'I']
    if len(infected) > 0:
        xCoord = [ag.x for ag in infected]
        yCoord = [ag.y for ag in infected]
    
    suspected = [ag for ag in agentsList if ag.status == 'S']
    if len(suspected) > 0:
        xCoord = [ag.x for ag in suspected]
        yCoord = [ag.y for ag in suspected]

    recovered = [ag for ag in agentsList if ag.status == 'R']
    if len(recovered) > 0:
        xCoord = [ag.x for ag in recovered]
        yCoord = [ag.y for ag in recovered]

    


def returnAvgRate():
    avgRateForSupsceptible = 0
    for ag in agentsList:
        if(ag.status == 'S'):
            avgRateForSupsceptible += ag.getInfectionRate()
    avgRate = len(agentsList) / avgRateForSupsceptible
    return round(avgRate, 2)
        
def initialize(infRate, maskRate, sanitizerRate, initPop):
    global agentsList
    agentsList = initializeAgents(infRate, maskRate, sanitizerRate, initPop)
        
def update_one_agent():
    global agentsList
    
    selectTwoAgentsRandom = random.sample(agentsList, 2)
    ag = selectTwoAgentsRandom[0]
    ag2 = selectTwoAgentsRandom[1]
    
    XnoiseLevel = random.randint(-50, 50)
    YnoiseLevel = random.randint(-50, 50)
                
    try:
        pixelColor = im.getpixel((ag.x, ag.y))
        pixelcolorAfterMovement = im.getpixel((ag.x + XnoiseLevel, ag.y + YnoiseLevel))
        if(pixelcolorAfterMovement in validColorZones and pixelColor in validColorZones):
            ag.x += XnoiseLevel
            ag.y += YnoiseLevel
    except IndexError as e:
        print(e)
        pass
    if(ag.id_no != ag2.id_no):
        checkDistanceBetween(ag,ag2)

def checkDistanceBetween(ag,ag2):
    distanceBetween = np.linalg.norm([ag.x-ag2.x,ag.y-ag2.y], ord = 2)
    if(distanceBetween <= 200):
        ag.startInfecting(ag, ag2)
    


    
def update():
    global agentsList
    t = 0.
    while t < 1. and len(agentsList) > 0:
        t += 1. / len(agentsList)
        update_one_agent()



def getInfectionRateNetwork(sorted_pop):
    totalInfectionRate=[]
    sorted_pop_arr = sorted_pop.tolist()
    for i in range(len(sorted_pop_arr)):
        initialize(sorted_pop_arr[i][0],sorted_pop_arr[i][1],sorted_pop_arr[i][2],sorted_pop_arr[i][3])
        observe()
        update()
        avgRate = returnAvgRate()
        totalInfectionRate.append(avgRate)
    return totalInfectionRate

