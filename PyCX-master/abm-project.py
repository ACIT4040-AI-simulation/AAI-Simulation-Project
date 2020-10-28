import pycxsimulator
from pylab import *
from agent import agent
from classRoom import classRoom
import json
import random
import copy as cp
p_init = 1000. #initial population

#infected ppl start from one
inf_rate = 0.10 # initial infaction rate in a population
mask_rate = 0.4 # percentage of mask users
dr = 1.0 # death rate of infected ppl
rr = 0.1 # recovery rate

f_init = 0.10 # initial fox population
mA = 0.05 # magnitude of movement of agents move
df = 0.1 # death rate of foxes when there is no food
rf = 0.5 # reproduction rate of foxes

cd = 0.05 # radius for collision detection
cdsq = cd ** 2
sdata = []
idata = []
# =============================================================================
    
def upload_agents_json(fileName):
    agenList = json.load(open(fileName))
    agentObjList = []

    for agentObj in agenList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'], agentObj['antibact'], agentObj['socialDistance'])
        agentObjList.append(temp)
    return agentObjList

def upload_classroom_json(fileName):
    classRoomList = json.load(open(fileName))
    classAgentsList = []

    for classroom in classRoomList:
        temp = classRoom(classroom['class_id'], classroom['class_type'], classroom['length'], classroom['width'], classroom['sitting_capacity'], classroom['cleaning_cycle'], classroom['clean_status'], classroom['antibac_dispenser'], classroom['ventilation_grade'])
        classAgentsList.append(temp)
    return classAgentsList    

def initializeAgents():
    agentsList = upload_agents_json("agent1000.json")
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
        ag.x = random.random()
        ag.y = random.random()
    return agentsList

def initializeRooms():
    classRoomList = upload_classroom_json('classrooms2.json')
    return classRoomList
        
def alocateAgentsinclass(agentlist, roomlist):
    x = 0
    for ag in agentlist:
        roomlist[x%15].agentsList.append(ag)
        ag.whereAmI = roomlist[x%15]
        x+=1
        
def initialize():
    global agentsList,inf_data,classRoomList,sdata, idata

    agentsList = initializeAgents()
    classRoomList = initializeRooms()
        
    alocateAgentsinclass(agentsList, classRoomList)
    
def observe():
    global agentsList, classRoomList, sdata, idata
    
    no_classes = len(classRoomList)
    print('no classes = ', no_classes )
    row = 6
    col = 3
    
    for i in range(15):  
        subplot(row, col, i+1)
        cla()
        infected = [ag for ag in classRoomList[i].agentsList if ag.status == 'I']
        if len(infected) > 0:
            x = [ag.x for ag in infected]
            y = [ag.y for ag in infected]
            plot(x, y, 'ro')
        
        suspected = [ag for ag in classRoomList[i].agentsList if ag.status == 'S']
        if len(suspected) > 0:
            x = [ag.x for ag in suspected]
            y = [ag.y for ag in suspected]
            plot(x, y, 'b.')
        axis('image')
        axis([0, 1, 0, 1]) # we will scale it acording to the size
        title('classRoom ')
   
    subplot(row,col , 17)
    cla()
    plot(sdata, label = 'prey')
    plot(idata, label = 'predator')
    legend()             

def update_one_agent():
    global agentsList
    if agentsList == []:
        return

    ag = choice(agentsList)
    # simulating random movement
    m = mA
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    classroom = ag.whereAmI
    neighbors = [nb for nb in classroom.agentsList if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
    print('Gorebetoch =', len(neighbors))
    ag.behavior(neighbors)
    
def update():
    global agentsList, classRoomList, sdata, idata
    t = 0.
    while t < 1. and len(agentsList) > 0:
        t += 1. / len(agentsList)        
        update_one_agent()

    sdata.append(sum([1 for x in agentsList if x.status == 'S']))
    idata.append(sum([1 for x in agentsList if x.status == 'I']))

pycxsimulator.GUI().start(func=[initialize, observe, update])