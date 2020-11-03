from random import choice
import pycxsimulator
from agent import agent
import matplotlib.pyplot as plt
from matplotlib.pyplot import axis, title
from matplotlib.patches import Polygon
import json
import random
import geopandas
import os


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

#buildingID 471, id 3991, 4th floor id 1772  "floorOutlineId": 1146047,
fig,ax = plt.subplots()

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
    p = None
    for floor in pois:
        xyCoord = floor['geometry']['coordinates']
        if (floor['floorId'] == 1772 and floor['title'] != None):
            #print("Room: " ,floor['title'], "\n Coordinates:  \n", floor['geometry'], "\n")
            for coordinates in floor['geometry']['coordinates']:
                p = Polygon(coordinates, facecolor = '#CEBBB7')
                ax.add_patch(p)
                center = find_center_of_polygon(coordinates)
                ax.text(center[0], center[1], floor['title'], ha="center", family='sans-serif', size=5)
        if(floor['floorId'] == 1772 and floor['title'] == None):
            #print("Room: " ,floor['title'], "\n Coordinates:  \n", floor['geometry'], "\n")
            ax.plot(xyCoord[0],xyCoord[1], 'g+')

def createFloorOutline():
    shapefile = geopandas.read_file(os.path.abspath(os.path.dirname(__file__)) + "/geoShapeFile/layers/POLYGON.shp")
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
        ax.plot(xCoord, yCoord, 'ro')
    
    suspected = [ag for ag in agentsList if ag.status == 'S']
    if len(suspected) > 0:
        xCoord = [ag.x for ag in suspected]
        yCoord = [ag.y for ag in suspected]
        ax.plot(xCoord, yCoord, 'b.')
    createFloorOutline()
    plot_4thfloor_rooms()


        
def initialize():
    print("initialize")
    global agentsList
    agentsList = initializeAgents()
    title('C-19 Mobility fourth floor P35')


        
def update_one_agent():
    global agentsList
    if agentsList == []:
        return

    ag = choice(agentsList)
    XnoiseLevel = random.uniform(-0.000050, 0.000050)
    YnoiseLevel = random.uniform(-0.0000300,0.0000300)
    
    ag.x =  (ag.x + XnoiseLevel) if (ag.x + XnoiseLevel) <= 100 else 100-(ag.x + XnoiseLevel)
    ag.y +=  YnoiseLevel
    axis('scaled')

    
    
def update():
    global agentsList
    t = 0.
    while t < 1. and len(agentsList) > 0:
        t += 1. / len(agentsList)
        
        update_one_agent()

pycxsimulator.GUI().start(func=[initialize, observe, update])

