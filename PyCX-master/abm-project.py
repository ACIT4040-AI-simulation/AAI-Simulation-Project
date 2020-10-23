import pycxsimulator
from pylab import *
from agent import agent
from classRoom import classRoom
import json
import random



import copy as cp
p_init = 1000. #initial population

inf_rate = 0.10 # initial infaction rate in a population
mask_rate = 0.4 # percentage of mask users
dr = 1.0 # death rate of infected ppl
rr = 0.1 # recovery rate

f_init = 0.10 # initial fox population
mf = 0.05 # magnitude of movement of foxes
df = 0.1 # death rate of foxes when there is no food
rf = 0.5 # reproduction rate of foxes

cd = 0.02 # radius for collision detection
cdsq = cd ** 2
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
        ag.whereAmI = roomlist[x%15].class_id
        x+=1
        
def initialize():
    global agentsList,inf_data, classRoomList

    agentsList = initializeAgents()
    classRoomList = initializeRooms()
        
    alocateAgentsinclass(agentsList, classRoomList)
    
def observe():
    global agentsList, classRoomList
    
    no_classes = len(classRoomList)
    print('no classes = ', no_classes )
    row = 5
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
        axis([0, 1, 0, 1])
        title('classRoom ')
        
        
# =============================================================================
#     subplot(2, 3, 2)
#     cla()
#     infected = [ag for ag in classRoomList[1].agentsList  if ag.status == 'I']
#     if len(infected) > 0:
#         x = [ag.x for ag in infected]
#         y = [ag.y for ag in infected]
#         plot(x, y, 'ro')
#     
#     suspected = [ag for ag in classRoomList[1].agentsList  if ag.status == 'S']
#     if len(suspected) > 0:
#         x = [ag.x for ag in suspected]
#         y = [ag.y for ag in suspected]
#         plot(x, y, 'b.')
#     axis('image')
#     axis([0, 1, 0, 1])
#     title('classRoom 2')
# 
#     subplot(2, 3, 3)
#     cla()
#     infected = [ag for ag in classRoomList[0].agentsList if ag.status == 'I']
#     if len(infected) > 0:
#         x = [ag.x for ag in infected]
#         y = [ag.y for ag in infected]
#         plot(x, y, 'ro')
#     
#     suspected = [ag for ag in classRoomList[0].agentsList if ag.status == 'S']
#     if len(suspected) > 0:
#         x = [ag.x for ag in suspected]
#         y = [ag.y for ag in suspected]
#         plot(x, y, 'b.')
#     axis('image')
#     axis([0, 1, 0, 1])
#     title('classRoom 3')
#     
#     subplot(2, 3, 4)
#     cla()
#     infected = [ag for ag in classRoomList[1].agentsList  if ag.status == 'I']
#     if len(infected) > 0:
#         x = [ag.x for ag in infected]
#         y = [ag.y for ag in infected]
#         plot(x, y, 'ro')
#     
#     suspected = [ag for ag in classRoomList[1].agentsList  if ag.status == 'S']
#     if len(suspected) > 0:
#         x = [ag.x for ag in suspected]
#         y = [ag.y for ag in suspected]
#         plot(x, y, 'b.')
#     axis('image')
#     axis([0, 1, 0, 1])
#     title('classRoom 4')
#    
#     subplot(2, 3, 5)
#     cla()
#     infected = [ag for ag in classRoomList[1].agentsList  if ag.status == 'I']
#     if len(infected) > 0:
#         x = [ag.x for ag in infected]
#         y = [ag.y for ag in infected]
#         plot(x, y, 'ro')
#     
#     suspected = [ag for ag in classRoomList[1].agentsList  if ag.status == 'S']
#     if len(suspected) > 0:
#         x = [ag.x for ag in suspected]
#         y = [ag.y for ag in suspected]
#         plot(x, y, 'b.')
#     axis('image')
#     axis([0, 1, 0, 1])
#     title('classRoom 4')
# 
#     subplot(2, 3, 6)
#     cla()
#     infected = [ag for ag in classRoomList[1].agentsList  if ag.status == 'I']
#     if len(infected) > 0:
#         x = [ag.x for ag in infected]
#         y = [ag.y for ag in infected]
#         plot(x, y, 'ro')
#     
#     suspected = [ag for ag in classRoomList[1].agentsList  if ag.status == 'S']
#     if len(suspected) > 0:
#         x = [ag.x for ag in suspected]
#         y = [ag.y for ag in suspected]
#         plot(x, y, 'b.')
#     axis('image')
#     axis([0, 1, 0, 1])
#     title('classRoom 4')
#    
# =============================================================================

def update_one_agent():
    global agentsList
    if agentsList == []:
        return

    ag = choice(agentsList)

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
    global agentList, classRoomList
    t = 0.
    while t < 1. and len(agents) > 0:
        t += 1. / len(agents)
        #update_one_agent()

pycxsimulator.GUI().start(func=[initialize, observe, update])
