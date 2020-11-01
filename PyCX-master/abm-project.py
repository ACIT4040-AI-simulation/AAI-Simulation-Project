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
mA = 0.05 # magnitude of movement of agents move
df = 0.1 # death rate of foxes when there is no food
rf = 0.5 # reproduction rate of foxes

cd = 0.02 # radius for collision detection
cdsq = cd ** 2
# =============================================================================
    
def upload_agents_json(filepath):
    with open('PyCX-master/'+filepath, 'r') as data: 
        AGENT_DATA = json.load(data)
    AGENT_ARRAY = []

    for agent in AGENT_DATA:
        #temp = agent(agent['id_no'], agent['age'], agent['gender'], agent['status'], agent['mask'], agent['antibact'], agent['socialDistance'])
        AGENT_ARRAY.append(agent)
    return AGENT_ARRAY


def upload_classroom_json(filepath):
    with open('PyCX-master/'+filepath, 'r') as data: 
        CLASSROOM_DATA = json.load(data)
    CLASS_AGENTS_ARRAY = []

    for classroom in CLASSROOM_DATA:
        #temp = classRoom(classroom['class_id'], classroom['class_type'], classroom['length'], classroom['width'], classroom['sitting_capacity'], classroom['cleaning_cycle'], classroom['clean_status'], classroom['antibac_dispenser'], classroom['ventilation_grade'])
        CLASS_AGENTS_ARRAY.append(classroom)
    return CLASS_AGENTS_ARRAY    

def initializeAgents():
    AGENTS_LIST = upload_agents_json("agent1000.json")
    n_inf_agents = p_init * inf_rate
    
    #randomly assighn mask to the population as per rate of mask usage data
    MASKED_LIST = random.sample(AGENTS_LIST,int(p_init*mask_rate))
    for ag in MASKED_LIST:
        ag["mask"]= True
        
    #randomly make ppl infected as per rate of infection rate data
    INFECTED_LIST = random.sample(AGENTS_LIST,int(p_init*inf_rate))
    for ag in INFECTED_LIST:
        ag["status"]= 'I'
    
#this loop will be taken out to classrooms acording to the sizes.
    for ag in AGENTS_LIST:
        ag["x"] = random.random()
        ag["y"] = random.random()
    return AGENTS_LIST

def initializeRooms():
    CLASSROOM_DATA = upload_classroom_json('classrooms2.json')
    return CLASSROOM_DATA
        
def alocateAgentsinclass(agentlist, roomlist):
    x = 0
    for ag in agentlist:
       # roomlist[x%15].AGENTS_LIST.append(ag)
        ag['whereAmI'] = roomlist[x%15]
        x+=1
        
def initialize():
    global AGENTS_LIST,inf_data, CLASSROOM_DATA

    AGENTS_LIST = initializeAgents()
    CLASSROOM_DATA = initializeRooms()
        
    alocateAgentsinclass(AGENTS_LIST, CLASSROOM_DATA)
    
def observe():
    global AGENTS_LIST, CLASSROOM_DATA
    
    no_classes = len(CLASSROOM_DATA)
    print('no classes = ', no_classes )
    row = 5
    col = 3
    
    for i in range(15):  
        subplot(row, col, i+1)
        cla()
        infected = [ag for ag in CLASSROOM_DATA[i] if ag.status == 'I']
        if len(infected) > 0:
            x = [ag.x for ag in infected]
            y = [ag.y for ag in infected]
            plot(x, y, 'ro')
        
        suspected = [ag for ag in CLASSROOM_DATA[i].AGENTS_LIST if ag.status == 'S']
        if len(suspected) > 0:
            x = [ag.x for ag in suspected]
            y = [ag.y for ag in suspected]
            plot(x, y, 'b.')
        axis('image')
        axis([0, 1, 0, 1])
        title('classRoom ')
        

def update_one_agent():
    global AGENTS_LIST
    if AGENTS_LIST == []:
        return

    ag = choice(AGENTS_LIST)

    # simulating random movement
    m = mA
    ag.x += uniform(-m, m)
    ag.y += uniform(-m, m)
    ag.x = 1 if ag.x > 1 else 0 if ag.x < 0 else ag.x
    ag.y = 1 if ag.y > 1 else 0 if ag.y < 0 else ag.y

    # detecting collision and simulating death or birth
# =============================================================================
#     neighbors = [nb for nb in agents if nb.type != ag.type
#                  and (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
# 
# =============================================================================
    classroom = ag.whereAmI
    neighbors = [nb for nb in classroom.AGENTS_LIST if (ag.x - nb.x)**2 + (ag.y - nb.y)**2 < cdsq]
    
def update():
    global AGENTS_LIST, CLASSROOM_DATA
    t = 0.
    while t < 1. and len(AGENTS_LIST) > 0:
        t += 1. / len(AGENTS_LIST)
        
        update_one_agent()

pycxsimulator.GUI().start(func=[initialize, observe, update])
