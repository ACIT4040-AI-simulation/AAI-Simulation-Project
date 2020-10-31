import pycxsimulator
from pylab import *
from agent import agent
import json
from random import randint as randint
import geopandas
from shapely.geometry import mapping, shape
import requests

import copy as cp
p_init = 100. #initial population

inf_rate = 0.10 # initial infaction rate in a population
mask_rate = 0.4 # percentage of mask users
# dr = 1.0 # death rate of infected ppl
# rr = 0.1 # recovery rate

f_init = 0.10 # initial fox population
mf = 0.05 # magnitude of movement of foxes
# df = 0.1 # death rate of foxes when there is no food
# rf = 0.5 # reproduction rate of foxes

cd = 0.02 # radius for collision detection
cdsq = cd ** 2

buildings_in_pilestredet = "https://api.mazemap.com/api/buildings/?campusid=53&srid=4326"
flooroutline_4th_floor = "https://api.mazemap.com/api/flooroutlines/?campusid=53&srid=4326" #Coordinates are now saved in geoJson file, so internet is no longer needed
POI_4th_floor = "https://api.mazemap.com/api/pois/562437/?srid=900913"

# =============================================================================
# class agent:
#     def __init__(self, status,mask,antibac, sdistance):
#         self.status = status #infected, recoverd, normal, exposed, dead,
#         self.mask = mask
#         self.antibac = antibac #rate 1-6
#         self.sdistance = sdistance # rate setted with local agency
#     def setStatus(self, status):
#         self.status = status
# =============================================================================
def connect_to_api(api_url):
    response = requests.get(api_url)
    extractP35data = response.json()['buildings'][11]
    floorOutlineId4thFloor = extractP35data['floors'][4]['floorOutlineId'] # "floorOutlineId": 1146047,
    #print(floorOutlineId4thFloor)
    return floorOutlineId4thFloor

def retriveJsonFromFile():
    shapefile = geopandas.read_file("PyCX-master/geoShapeFile/layers/POLYGON.shp")
    shapefile.plot()
    gca()
    axis('scaled')
    show()

def upload_json():
    agenList = json.load(open("PyCX-master/agentdata.json"))
    agentObjList = []

    for agentObj in agenList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'])
        agentObjList.append(temp)
    return agentObjList

def initialize():
    global agentsList,inf_data
    
# =============================================================================
    agentsList = upload_json()
#     
#     lectroom1= classRom(agentsList[0:100])
#     lectroom2= classRom(agentsList[100:200])
# ============================================================================
    
    inf_data = []
   
    n_inf_agents = p_init * inf_rate
    
    #randomly assighn mask to the population as per rate of mask usage data
    for i in range(int(p_init*mask_rate)):
        agentsList[randint(0, p_init-1)].mask= True
        
    #randomly make ppl infected as per rate of infection rate data
    for i in range(int(p_init*inf_rate)):
        agentsList[randint(0, p_init-1)].status= 'I'
    
    
    for ag in agentsList:
        ag.x = random()
        ag.y = random()
        
    
    

def observe():
    global agentsList, rdata, fdata

    subplot(1, 1, 1)
    cla()
    infected = [ag for ag in agentsList if ag.status == 'I']
    if len(infected) > 0:
        x = [ag.x for ag in infected]
        y = [ag.y for ag in infected]
        plot(x, y, 'ro')
    
    suspected = [ag for ag in agentsList if ag.status == 'S']
    if len(suspected) > 0:
        x = [ag.x for ag in suspected]
        y = [ag.y for ag in suspected]
        plot(x, y, 'b.')
    axis('image')
    axis([-1, 100, -1, 100])
    
# =============================================================================
# 
#     subplot(2, 1, 2)
#     cla()
#     plot(rdata, label = 'prey')
#     plot(fdata, label = 'predator')
#     legend()
# 
# =============================================================================
def update_one_agent():
    global agentsList
    if agents == []:
        return

    ag = choice(agents)

    # simulating random movement
    m = mr if ag.type == 'r' else mf
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision and simulating death or birth
    neighbors = [nb for nb in agents if nb.type != ag.type
                 and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]

    if ag.type == 'r':
        if len(neighbors) > 0: # if there are foxes nearby
            if random() < dr:
                agents.remove(ag)
                return
        if random() < rr*(1-sum([1 for x in agents if x.type == 'r'])/nr):
            agents.append(cp.copy(ag))
    else:
        if len(neighbors) == 0: # if there are no rabbits nearby
            if random() < df:
                agents.remove(ag)
                return
        else: # if there are rabbits nearby
            if random() < rf:
                agents.append(cp.copy(ag))

def update():
    global agents, rdata, fdata
    t = 0.
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        #update_one_agent()

    # rdata.append(sum([1 for x in agents if x.type == 'r']))
    # fdata.append(sum([1 for x in agents if x.type == 'f']))


#connect_to_api(buildings_in_pilestredet)
retriveJsonFromFile()
#pycxsimulator.GUI().start(func=[initialize, observe, update])

