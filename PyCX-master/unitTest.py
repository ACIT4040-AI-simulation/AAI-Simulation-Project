#This file is executing unit teting
import os
from evo_agent import evo_agent as agent
from PIL import Image as img
import json
import random
import numpy as np
import os

#import initializeAgents.py
#import initialize
#import observe
#import returnAvgRate
#import upload_agents_json
#import getInfectionRate


imgPath = os.path.abspath(os.path.dirname(__file__)) + "/p35-4thfloor_withdoors.png"
im = img.open(imgPath)

DOOR_COLOR = im.getpixel((985, 622))
FLOOR_COLOR = im.getpixel((1113, 329))
NUANCE_COLOR = (215, 201, 198, 255)

validColorZones = [ DOOR_COLOR, FLOOR_COLOR, NUANCE_COLOR]


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
This will change the percentage of Infected agents according the Initial agentsList
"""
def changePercentageOfInfectedAgents(infectedPercentage, agentsList):
    numberOfAgents = float(len(agentsList)) * infectedPercentage
    agentList = random.sample(agentsList, round(numberOfAgents))
    for i in agentList:
        i.status = 'I'

    return agentsList





"""
This will change the percentage of Infected agents according the Initial agentsList
"""


def changePercentageOfMaskUsers(maskPercentage, agentsList):
    numberOfAgents = float(len(agentsList)) * maskPercentage
    agentList = random.sample(agentsList, round(numberOfAgents))
    for i in agentList:
        i.mask = True

    return agentsList


"""
This will change the percentage of Infected agents according the Initial agentsList
"""


def changePercentageOfSanitizerUsers(sanitizerPercentage, agentsList):
    numberOfAgents = float(len(agentsList)) * sanitizerPercentage
    agentList = random.sample(agentsList, round(numberOfAgents))
    for i in agentList:
        i.sanitizer = True

    return agentsList


#Unit Test function for initializeAgents() function
def test_initializeAgents():
    classgroup = [1,2,3]
    x_coordinates = []
    y_coordinates = []

    for i in range(360,800):
        x_coordinates.append(i)
    for i in range(2026,2160):
        x_coordinates.append(i)
    for i in range(200,500):
        x_coordinates.append(i)
    for i in range(1300,1400):
        x_coordinates.append(i)

    for i in range(900,1050):
        y_coordinates.append(i)
    for i in range(921, 1129):
        y_coordinates.append(i)
    for i in range(1180,1300):
        y_coordinates.append(i)
    for i in range(126,306):
        y_coordinates.append(i)

    #test_agentsList = InitializeAgents(0.8, 0.4, 0.8, 50)
    test_agentsList = upload_agents_json(os.path.abspath(os.path.dirname(__file__)) + "/100_Agents.json", 0.8,0.4,0.8,50)
    classroom_list=[]
    x_list=[]
    y_list=[]

    for value in test_agentsList:
        if value.classroom in classgroup:
            classroom_list.append(value)
        if value.x in x_coordinates:
            x_list.append(value)
        if value.y in y_coordinates:
            y_list.append(value)

    assert len(classroom_list) == 50
    assert len(x_list) == 50
    assert len(y_list) == 50

#Unit Test function for observe() function
def test_observe():
    global test_agentsList
    test_agentsList = upload_agents_json(os.path.abspath(os.path.dirname(__file__)) + "/100_Agents.json", 0.8, 0.4, 0.8,50)
    infected = [ag for ag in agentsList if ag.status == 'I']
    if len(infected) > 0:
        xCoord = [ag.x for ag in infected]
        yCoord = [ag.y for ag in infected]
        xi=len(xCoord)
        yi=len(yCoord)
    suspected = [ag for ag in agentsList if ag.status == 'S']
    if len(suspected) > 0:
        xCoord = [ag.x for ag in suspected]
        yCoord = [ag.y for ag in suspected]
        xs=len(xCoord)
        ys=len(yCoord)

    recovered = [ag for ag in agentsList if ag.status == 'R']
    if len(recovered) > 0:
        xCoord = [ag.x for ag in recovered]
        yCoord = [ag.y for ag in recovered]
        xr=len(xCoord)
        yr=len(yCoord)

    assert len(xi)==len(yi)
    assert len(xs) == len(ys)
    assert len(xr) == len(yr)
    assert len(infected) == len(xi)
    assert len(suspected) == len(ys)
    assert len(recovered) == len(xr)


#Unit Test function for returnAvgRate() function


#Unit Test function for initialize() function
def test_initialize():
    #global agentsList
    x_count=0
    y_count=0
    test_agents = initializeAgents(0.7,0.3,0.8,80)
    for agent in test_agents:
        if agent.x in validColorZones:
            x_count+=1
        if agent.y in validColorZones:
            y_count+=1

    assert x_count==80
    assert y_count==80
