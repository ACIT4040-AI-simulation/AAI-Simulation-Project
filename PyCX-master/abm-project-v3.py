from random import choice
import cv2
from matplotlib import colors
from numpy.core.shape_base import block
import pycxsimulator
from evo_agent import evo_agent as agent
from PIL import Image as img
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, title
import matplotlib.image as mpimg
from matplotlib.patches import Polygon
from matplotlib.widgets import Button
import matplotlib.colors as colors
from shapely.geometry.polygon import Polygon as ply
from shapely.geometry.point import Point
import json
import random
import geopandas
import numpy as np
import os


p_init = 40 #initial population

inf_rate = 0.10 # initial infaction rate in a population
mask_rate = 0.4 # percentage of mask users
dr = 1.0 # death rate of infected ppl
rr = 0.1 # recovery rate

f_init = 0.10 # initial fox population
mA = 0.05 # magnitude of movement of agents move
df = 0.1 # death rate of foxes when there is no food
rf = 0.5 # reproduction rate of foxes

cd = 0.02 # radius for collision detection
cdsq = cd ** 2
# =============================================================================
imgPath = os.path.abspath(os.path.dirname(__file__)) + "/p35-4thfloor_withdoors.png"
p35_outline = []
numberOfAgentsInP35 = 0
#buildingID 471, id 3991, 4th floor id 1772  "floorOutlineId": 1146047,
fig,ax = plt.subplots()

pycx = pycxsimulator.GUI()
"""
minX = 10.734699459776635
maxX = 10.735943200721804
minY = 59.91914	    
maxY = 59.919899000945
"""

im = img.open(imgPath) # Can be many different formats.
palette = im.getpixel((1113, 329))
print(palette, "\n")
picture = mpimg.imread(imgPath)

validColorZones = [
    im.getpixel((985, 622)), #Doorcolor
    im.getpixel((1113, 329)), #FloorColor
    (215, 201, 198, 255)
    ]




"""
This will change the percentage of Infected agents according the Initial agentsList
"""
def changePercentageOfInfectedAgents(numberOfAgents, agentsList):
    agentList = random.sample(agentsList,numberOfAgents)
    for i in agentList:
        i.status = 'I'

    return agentsList

"""
This will change the percentage of Infected agents according the Initial agentsList
"""
def changePercentageOfMaskUsers(numberOfAgents, agentsList):
    agentList = random.sample(agentsList,numberOfAgents)
    for i in agentList:
        i.mask = True    
    
    return agentsList

"""
This will change the percentage of Infected agents according the Initial agentsList
"""
def changePercentageOfSanitizerUsers(numberOfAgents, agentsList):
    agentList = random.sample(agentsList,numberOfAgents)
    for i in agentList:
        i.sanitizer = True    
    
    return agentsList

    
def upload_agents_json(fileName, initialPopulation):
    jsonAgentList = json.load(open(fileName))
    agentObjList = []

    for agentObj in jsonAgentList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'], agentObj['infectionRate'])
        agentObjList.append(temp)

    agentObjList = changePercentageOfInfectedAgents(initialPopulation, agentObjList)
    agentObjList = changePercentageOfMaskUsers(initialPopulation, agentObjList)
    agentObjList = changePercentageOfSanitizerUsers(initialPopulation, agentObjList)
    print(len(agentObjList))
    maskCount = 0
    for i in agentObjList:
        if(i.mask == True):
            maskCount+=1
    print(maskCount)

    return agentObjList

 
"""
 This will have 4 parameters distance (float), mask (float), sanitizer (float), initial population (INT)

"""
def initializeAgents(initPop):
    global p35_outline
    print("initializeAgents")
    agentsList = upload_agents_json(os.path.abspath(os.path.dirname(__file__)) + "/100_Agents.json", initPop)
    for ag in agentsList:
        ag.classGroup = random.randint(1,3)
        ag.x = random.randint(600,1800)
        ag.y = random.randint(300,1200)
       
    """
        40 / 100 
        change initializaion position of agents until probaility is reached. 
        Probabilitycounter = 0;
        ag = choice ag2 chouce, checkDIstance(ag1,ag2): Probabilitycounter++; 5 / 100 = 0.05
    """
            
    return agentsList


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

    #print(len(agentsList), "IN OBSERVE", len(suspected), len(infected))
    plt.title('Minimize this figure')
    fig.suptitle('C-19 Mobility : {} suspected and {} infected'.format(len(suspected), len(infected)))
    plotImage()

def plotImage():    
    ax.imshow(picture)
    axis('image')
        
def initialize():
    global agentsList
    agentsList = initializeAgents(p_init)
        
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

def checkDistanceBetween(ag,ag2):
    distanceBetween = np.linalg.norm([ag.x-ag2.x,ag.y-ag2.y], ord = 2)
    if(distanceBetween <= 20):
        #print(distanceBetween, "\n", (ag.x,ag.y), (ag2.x,ag2.y)   ,"\n")
        ag.startInfecting(ag, ag2)
    


    
def update():
    global agentsList
    t = 0.
    ax.margins(1)
    while t < 1. and len(agentsList) > 0:
        t += 1. / len(agentsList)
        update_one_agent()



pycx.start(func=[initialize, observe, update])

