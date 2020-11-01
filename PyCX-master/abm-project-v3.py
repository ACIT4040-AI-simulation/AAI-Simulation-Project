from datetime import time
from random import choice, uniform
import pycxsimulator
from agent import agent
from classRoom import classRoom
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, cla, plot, title
from matplotlib.patches import Polygon
from shapely.geometry import mapping, shape
import json
import random
import geopandas
import requests
import numpy as np
import copy as cp


p_init = 100. #initial population

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

buildings_in_pilestredet = "https://api.mazemap.com/api/buildings/?campusid=53&srid=4326" #buildingID 471, id 3991, 4th floor id 1772  "floorOutlineId": 1146047,
flooroutline_4th_floor = "https://api.mazemap.com/api/flooroutlines/?campusid=53&srid=4326" #Coordinates are now saved in geoJson file, so internet is no longer needed
POI_4th_floor = "https://api.mazemap.com/api/pois/562437/?srid=900913"
POI_ON_P35 = "https://api.mazemap.com/api/campus/53/pois/?identifier=P35-P35&floorId=1772&srid=4326"

fig,ax = plt.subplots()


def connect_to_api(api_url):
    response = requests.get(api_url)
    pois = response.json()['pois']
    p = None
    for floor in pois:
        if (floor['floorId'] == 1772 and floor['title'] != None):
            #print("Room: " ,floor['title'], "\n Coordinates:  \n", floor['geometry'], "\n")
            for coordinates in floor['geometry']['coordinates']:
                y = np.array(coordinates)
                p = Polygon(y, facecolor = '#CEBBB7')
                ax.add_patch(p)
        if(floor['floorId'] == 1772 and floor['title'] == None):
            #print("Room: " ,floor['title'], "\n Coordinates:  \n", floor['geometry'], "\n")
            coordinates = floor['geometry']['coordinates']
            ax.plot(coordinates[0],coordinates[1], 'g+')


def retriveJsonFromFile():
    shapefile = geopandas.read_file("PyCX-master/geoShapeFile/layers/POLYGON.shp")
    # print(shapefile.to_csv()) to get values 
    shapefile.plot(ax = ax,color='white', edgecolor='k',linewidth = 4)
    
def upload_agents_json(fileName):
    agenList = json.load(open(fileName))
    agentObjList = []

    for agentObj in agenList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'])
        agentObjList.append(temp)
    return agentObjList

 

def initializeAgents():
    print("initializeAgents")
    agentsList = upload_agents_json("PyCX-master/agentdata.json")
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
        ag.x = random.uniform(10.734699459776635,10.735943200721804)
        ag.y = random.uniform(59.91914,59.919899000945)
    return agentsList
        
def observe():
    global agentsList
    ax.cla()
    infected = [ag for ag in agentsList if ag.status == 'I']
    if len(infected) > 0:
        xCoord = [ag.x for ag in infected]
        yCoord = [ag.y for ag in infected]
        #print(xCoord)
        ax.plot(xCoord, yCoord, 'ro')
    
    suspected = [ag for ag in agentsList if ag.status == 'S']
    if len(suspected) > 0:
        xCoord = [ag.x for ag in suspected]
        yCoord = [ag.y for ag in suspected]
        ax.plot(xCoord, yCoord, 'b.')
    title('C-19 Mobility fourth floor P35')
    #retriveJsonFromFile()
    #connect_to_api(POI_ON_P35)


        
def initialize():
    print("initialize")
    global agentsList
    agentsList = initializeAgents()
    retriveJsonFromFile()
    connect_to_api(POI_ON_P35)

        
def update_one_agent():
    global agentsList
    if agentsList == []:
        return

    ag = choice(agentsList)
    noiseLevel = random.uniform(-0.000001, 0.000008)
    # simulating random movement
    #ag.x += random.uniform(-0.000001, 0.000008)
    #ag.y += random.uniform(-0.000001, 0.000009)
    ag.x =  (ag.x + noiseLevel) if (ag.x + noiseLevel) <= 100 else 100-(ag.x + noiseLevel)
    ag.y +=  noiseLevel
    axis('scaled')

    
    
def update():
    global agentsList
    t = 0.
    while t < 1. and len(agentsList) > 0:
        t += 1. / len(agentsList)
        
        update_one_agent()

pycxsimulator.GUI().start(func=[initialize, observe, update])