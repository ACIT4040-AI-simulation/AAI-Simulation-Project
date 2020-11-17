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


p_init = 20. #initial population

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
pix = im.load()
picture = mpimg.imread(imgPath)

validColorZones = [
    pix[622,985], #Doorcolor
    pix[329,1113], #FloorColor
    (215, 201, 198, 255)
    ]

sobelIMG = cv2.imread(imgPath,0)
edges = cv2.Canny(sobelIMG,100,200)
ax.imshow(picture)


def find_center_of_polygon(vertexes):
     _x_list = [vertex [0] for vertex in vertexes]
     _y_list = [vertex [1] for vertex in vertexes]
     _len = len(vertexes)
     _x = sum(_x_list) / _len
     _y = sum(_y_list) / _len
     return(_x, _y)

def plot_4thfloor_rooms():
    response = json.load(open(os.path.abspath(os.path.dirname(__file__)) + "/P35_4thfloor_rooms.json"))
    pois = response['pois']
    for floor in pois:
        xyCoord = floor['geometry']['coordinates']
        if (floor['floorId'] == 1772 and floor['title'] != None):
            #print("Room: " ,floor['title'], "\n Coordinates:  \n", floor['geometry'], "\n")
            drawRoomsAndAnnotateLabels(floor)
        #if(floor['floorId'] == 1772 and floor['title'] == None):
            #print("Room: " ,floor['title'], "\n Coordinates:  \n", floor['geometry'], "\n")
         #   ax.plot(xyCoord[0],xyCoord[1], 'g+')

def drawRoomsAndAnnotateLabels(floor):
    for coordinates in floor['geometry']['coordinates']:
        p = Polygon(coordinates, fc = "#D1CBCB")  #fc = rgb = 209,203,203
        ax.add_patch(p)
        #givelabelstoclassroom(coordinates, floor) uncomment if seeing labels
        checkIfAgentIsInARoom(coordinates, floor)


def givelabelstoclassroom(coordinates, floor):
    center = find_center_of_polygon(coordinates)
    ax.text(center[0], center[1], floor['title'], ha="center", family='sans-serif', size=5)


def checkIfAgentIsInARoom(coordinates, floor):
    global agentsList, numberOfAgentsInP35
    for agent in agentsList:
        agentPoint = Point(agent.x,agent.y)
        isWithin = checkAgentInClassroom(agentPoint,ply(coordinates))
        if(isWithin):
            numberOfAgentsInP35 += 1
            agent.whereAmI = floor['poiId']
            #print(agent.id_no, " with coordinates ", agentPoint , " is inside ", floor['title'])
        # else:
        #     print("not within", agent.id_no)
        #     agentsList.remove(agent)

def checkAgentInClassroom(point, polygon):
    return point.within(polygon)


def createFloorOutline():
    response = json.load(open(os.path.abspath(os.path.dirname(__file__)) + "/P35_FloorOutline.geojson"))
    p35_outline = response['features'][0]['geometry']['coordinates']
    for coordinates in p35_outline:
        p = Polygon(coordinates, facecolor = '#FFFFFF', edgecolor='#000000',linewidth = 4)
        ax.add_patch(p)
    
def upload_agents_json(fileName):
    agenList = json.load(open(fileName))
    agentObjList = []

    for agentObj in agenList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'])
        agentObjList.append(temp)
    return agentObjList

 

def initializeAgents():
    global p35_outline
    print("initializeAgents")
    agentsList = upload_agents_json(os.path.abspath(os.path.dirname(__file__)) + "/agentdata.json")
    n_inf_agents = p_init * inf_rate
    
    #randomly assighn mask to the population as per rate of mask usage data
    maskedList = random.sample(agentsList,int(p_init*mask_rate))
    for ag in maskedList:
        ag.mask= True
        
    #randomly make ppl infected as per rate of infection rate data
    infectedList = random.sample(agentsList,int(p_init*inf_rate))
    for ag in infectedList:
        ag.status= 'I'
    
#this loop will be taken out to classrooms acording to the sizes.
    for ag in agentsList:
        ag.classGroup = random.randint(1,3)
        ag.x = random.randint(600,1800)
        ag.y = random.randint(300,1200)
        #ag.x = random.uniform(minX,maxX)
        #ag.y = random.uniform(minY,maxY)
        #getRGB_Color(ag)
        
            
    return agentsList

def getRGB_Color(ag):
    data = []
    data.append((ag.x, ag.y))
    im = plt.imshow(data)
    rgb = im.cmap(im.norm( (ag.x,ag.y) ))
    for color in rgb:
        getHex = colors.to_hex(color)
        print(getHex," \n---- ", color)
    return rgb

def observe():
    global agentsList, numberOfAgentsInP35
    numberOfAgentsInP35 = 0
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
    #createFloorOutline()
    #plot_4thfloor_rooms()
    #if(numberOfAgentsInP35 <= -1):
     #   pycx.running = False
        #print("Simulation stopped because number of agents inside reached 0")
    plt.title('Minimize this figure')
    #fig.suptitle('C-19 Mobility; {} students in P35'.format(numberOfAgentsInP35))
    plotImage()

def plotImage():    
    ax.imshow(picture)
    axis('image')



        
def initialize():
    print("initialize")
    global agentsList
    agentsList = initializeAgents()
        
def update_one_agent():
    global agentsList
    if agentsList == []:
        return

    ag = choice(agentsList)
    ag2 = choice(agentsList)
    
    XnoiseLevel = random.randint(-50, 50)
    YnoiseLevel = random.randint(-50,50)
                
    try:
        pixelColor = pix[ag.y, ag.x]
        pixelcolorAfterMovement = pix[ag.y + YnoiseLevel, ag.x + XnoiseLevel]
        if(pixelcolorAfterMovement in validColorZones and pixelColor in validColorZones):
            ag.x += XnoiseLevel
            ag.y += YnoiseLevel
    except IndexError as e:
        pass
    if(ag.id_no != ag2.id_no):
        checkDistanceBetween(ag,ag2)

def checkDistanceBetween(ag,ag2):
    distanceBetween = np.linalg.norm([ag.x-ag2.x,ag.y-ag2.y], ord = 2)
    if(distanceBetween < 40):
        #print(distanceBetween, "\n", (ag.x,ag.y), (ag2.x,ag2.y)   ,"\n")
        neighbors = []
        neighbors.append(ag)
        neighbors.append(ag2)
        ag.behavior(neighbors)
    
   
    
def update():
    global agentsList
    t = 0.
    ax.margins(1)
    while t < 1. and len(agentsList) > 0:
        t += 1. / len(agentsList)
        update_one_agent()



pycx.start(func=[initialize, observe, update])

