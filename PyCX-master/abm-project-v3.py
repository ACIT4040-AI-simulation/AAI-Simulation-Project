# -*- coding: utf-8 -*-
"""
Created on Sun Nov  22 23:30:47 2020

@author: Ilham Jilani, Kassahun Gedlu
"""

import pycxsimulator
from evo_agent import evo_agent as agent
from PIL import Image as img
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis
import matplotlib.image as mpimg
import json
import random
import numpy as np
import os


initPop = 70
infRate = 0.10
maskRate = 0.40
sanitizerRate = 0.60

imgPath = os.path.abspath(os.path.dirname(__file__)) + "/p35-4thfloor_withdoors.png"
fig, (ax, ax2, ax3) = plt.subplots(1,3)
pycx = pycxsimulator.GUI()

im = img.open(imgPath)
picture = mpimg.imread(imgPath)
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
        i.sanitizer = True    
    
    return agentsList

"""
This will first retrive the agents from a json file and manipulate their attributes and size based on the given parameters
"""
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
    agentsList = upload_agents_json(os.path.abspath(os.path.dirname(__file__)) + "/100_Agents.json", infRate, maskRate, sanitizerRate, initPop)
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

"""
This will update/observe the current values of the agents
"""
def observe():
    global agentsList
    ax.cla()

    infected = [ag for ag in agentsList if ag.status == 'I']
    if len(infected) > 0:
        xCoord = [ag.x for ag in infected]
        yCoord = [ag.y for ag in infected]
        ax.plot(xCoord, yCoord, 'r.')
    
    suspected = [ag for ag in agentsList if ag.status == 'S']
    if len(suspected) > 0:
        xCoord = [ag.x for ag in suspected]
        yCoord = [ag.y for ag in suspected]
        ax.plot(xCoord, yCoord, 'b.')

    recovered = [ag for ag in agentsList if ag.status == 'R']
    if len(recovered) > 0:
        xCoord = [ag.x for ag in recovered]
        yCoord = [ag.y for ag in recovered]
        ax.plot(xCoord, yCoord, 'g.')

    plt.title('Minimize this figure')
    fig.suptitle('C-19 Mobility : {} suspected, {} infected and {} recovered \n Time: {}'.format(len(suspected), len(infected), len(recovered) , pycx.currentStep))
    plotImage()

    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = 'S' , 'I', 'R'
    sizes = [len(suspected), len(infected), len(recovered)]
    explode = (0, 0, 0)
    ax2.cla()
    ax2.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax2.axis('equal') 
    
    ax3.plot(2, 1, 2)
    
    ax3.plot(pycx.currentStep, len(infected), color = 'red', marker = "o")
    ax3.plot(pycx.currentStep, len(suspected), color = 'blue', marker = "o")
    ax3.plot(pycx.currentStep, len(recovered), color = 'green', marker = "o")
    ax3.set(xlabel = "time", ylabel = "No of nodes")

    ax3.axis([0,200,0,100])
    if(pycx.currentStep == 50):
        returnAvgRate()

"""
This will return the average infection rate
"""
def returnAvgRate():
    pycx.running = False
    avgRateForSupsceptible = 0
    for ag in agentsList:
        if(ag.status == 'S'):
            avgRateForSupsceptible += ag.getInfectionRate()
    avgRate = len(agentsList) / avgRateForSupsceptible
    return round(avgRate, 2)

"""
This will plot the fourth floor of P35 in the figure
"""
def plotImage():    
    ax.imshow(picture)
    axis('image')

"""
This will initialize the agents
"""
def initialize():
    global agentsList
    agentsList = initializeAgents(infRate, maskRate, sanitizerRate, initPop)

"""
This will update the status, check neighbours and move the agent
"""
def update_one_agent():
    global agentsList
    if agentsList == []:
        return
    
    selectTwoAgentsRandom = random.sample(agentsList, 2)
    ag = selectTwoAgentsRandom[0]
    ag2 = selectTwoAgentsRandom[1]
    
    XnoiseLevel = random.randint(-50, 50)
    YnoiseLevel = random.randint(-50,50)
                
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

"""
This will check the distance between two agents, and check if the distance is 50 or less to investigate infection
"""
def checkDistanceBetween(ag,ag2):
    distanceBetween = np.linalg.norm([ag.x-ag2.x,ag.y-ag2.y], ord = 2)
    if(distanceBetween <= 50):
        #print(distanceBetween, "\n", (ag.x,ag.y), (ag2.x,ag2.y)   ,"\n")
        ag.startInfecting(ag, ag2)
    


"""
This will update the environment
"""
def update():
    global agentsList
    t = 0.
    while t < 1. and len(agentsList) > 0:
        t += 1. / len(agentsList)
        update_one_agent()



pycx.start(func=[initialize, observe, update])

