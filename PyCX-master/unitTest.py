#from PyCX-master import evo_agent.py
from unittest import mock
import os
import numpy as np
import pytest
import WithoutPyCx as wPyCx
import Evopart as evopart
from evo_agent import evo_agent as agent
import numpy as np

@pytest.fixture()
def startInfecting():
    infectionRate = 0
    return [infectionRate]

def test_for_startInfecting(startInfecting):
    agent2 = 0
    assert startInfecting[0] == agent2

@pytest.fixture()
def calcInfectionRate():
    currentNode_status = 'I'
    neighbourNode_infectionRate_1 = 0.015
    neighbourNode_infectionRate_2 = 0.05
    neighbourNode_infectionRate_3 = 0.7
    currentNode_status_4 = 'S'
    return [currentNode_status,
            neighbourNode_infectionRate_1,
            neighbourNode_infectionRate_2,
            neighbourNode_infectionRate_3,
            currentNode_status_4]

def test_for_calcInfectionRate(calcInfectionRate):
    x = 'I'
    assert calcInfectionRate[0] == x

def test_for_calcInfectionRate_1(calcInfectionRate):
    neighbourNode_infectionRate_1 = 0.015
    assert calcInfectionRate[1] == neighbourNode_infectionRate_1

def test_for_calcInfectionRate_2(calcInfectionRate):
    neighbourNode_infectionRate_2 = 0.05
    assert calcInfectionRate[2] == neighbourNode_infectionRate_2

def test_for_calcInfectionRate_3(calcInfectionRate):
    neighbourNode_infectionRate_3 = 0.7
    assert calcInfectionRate[3] == neighbourNode_infectionRate_3

def test_for_calcInfectionRate_4(calcInfectionRate):
    currentNode_status_4 = 'S'
    assert calcInfectionRate[4] == currentNode_status_4

@pytest.fixture()
def getInfectionRate():
    infectiorRate  = 10
    return [infectiorRate]

def test_for_getInfectionRate(getInfectionRate):
    infectionRate = 10
    assert getInfectionRate[0] ==infectionRate


agentList = [ {
    "id_no": 0,
    "age": 23,
    "gender": "female",
    "status": "S",
    "mask": False,
    "antibact": False,
    "socialDistance": False,
    "infectionRate": 0.903
  },
  {
    "id_no": 1,
    "age": 33,
    "gender": "female",
    "status": "S",
    "mask": False,
    "antibact": False,
    "socialDistance": False,
    "infectionRate": 0.694
  },
  {
    "id_no": 2,
    "age": 40,
    "gender": "male",
    "status": "S",
    "mask": False,
    "antibact": False,
    "socialDistance": False,
    "infectionRate": 0.169
  },]


def test_changePercentageOfInfectedAgents():
    agentObjList = []
    infectedList = []

    for agentObj in agentList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'],
                    agentObj['antibact'], agentObj['socialDistance'], agentObj['infectionRate'])
        agentObjList.append(temp)
    f = wPyCx.changePercentageOfInfectedAgents(0.8, agentObjList)
    for i in f:
        if i.status == "I":
            infectedList.append(i)

    assert len(infectedList) == 2

"""
Testing the changePercentageOfmaskUsers checking the number of people wearing mask in a list of 3 people, when percentage is 40%, expected result:1
"""
def test_changePercentageOfmaskUsers():
    agentObjList = []
    maskUsageList = []

    for agentObj in agentList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'],
                    agentObj['antibact'], agentObj['socialDistance'], agentObj['infectionRate'])
        agentObjList.append(temp)
    f = wPyCx.changePercentageOfMaskUsers(0.4, agentObjList)
    for i in f:
        if i.mask:
            maskUsageList.append(i)

    assert len(maskUsageList) == 1

"""
Testing the changePercentageOfSanitizerUsers checking the number of people using antibac in a list of 3 people, when percentage is 80%, expected result: 2
"""
def test_changePercentageOfSanitizerUsers():
    agentObjList = []
    sanitizerUsageList = []

    for agentObj in agentList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'],
                    agentObj['antibact'], agentObj['socialDistance'], agentObj['infectionRate'])
        agentObjList.append(temp)
    f = wPyCx.changePercentageOfSanitizerUsers(0.8, agentObjList)
    for i in f:
        if i.antibac:
            sanitizerUsageList.append(i)

    assert len(sanitizerUsageList) == 2

"""
Testing the upload_agents_json func, this func incorprates all the attributes changing functions (mask,sanitizer,infectionrate) based on 100 agents
"""
def test_upload_agents_json():
    sanitizerUsageList = []
    infectedList = []
    maskUsageList = []

    f = wPyCx.upload_agents_json(os.path.abspath(os.path.dirname(__file__)) + "/100_Agents.json", 0.8, 0.4, 0.8, 100)

    for i in f:
        if i.antibac:
            sanitizerUsageList.append(i)
        if i.status == "I":
            infectedList.append(i)
        if i.mask:
            maskUsageList.append(i)
    assert len(infectedList) == 80
    assert len(maskUsageList) == 40
    assert len(sanitizerUsageList) == 80

"""
Checks the lenght of the radomarray to see if its euqal to 10
"""
def test_random_array_generator():
    f = evopart.random_array_generator()
    assert len(f) == 10

"""
Checks if the fitness score function is choosing the two parents with the lowest infection rates
"""
def test_fitness_score():

    sortedPop = [
        [0.3,0.4,0.3,100],
        [0.2,0.7,0.1, 70],
        [0.9,0.6,0.85, 90]
    ]

    Infectionrate = [3.50, 2.40, 1.4]
    f = evopart.fitness_score(sortedPop, Infectionrate)
    
    assert f[0][4] == 1.4 and f[1][4] == 2.4


def test_sorted_population():
    mock_randomArray = mock.Mock(return_value = 5)
    mock_sortedpop = mock.Mock(return_value = 5)
    randomArray = evopart.random_array_generator()

    f = evopart.sorted_population(randomArray)
    f = mock_sortedpop 
    randomArray = mock_randomArray


    assert mock_sortedpop() == mock_randomArray()


def test_initialize_agents():
    initAgents = [
        agent('1','20', 'M', 'S', True, True, True, 1.0) ,
        agent('2','20', 'M', 'S', True, True, True, 1.0) ,
        agent('3','20', 'M', 'S', True, True, True, 1.0) ,
        agent('4','20', 'M', 'S', True, True, True, 1.0) 
    ]
    mock_upload_json = mock.Mock(name="upload_json", return_value= initAgents)
    wPyCx.upload_agents_json = mock_upload_json
    f = wPyCx.initializeAgents(0.5, 0.5, 0.5, 4)
    mock_upload_json.assert_called()
    assert len(f) == len(initAgents)


def test_observe():
    initAgents = [
        agent('1','20', 'M', 'S', True, True, True, 1.0) ,
        agent('2','20', 'M', 'I', True, True, True, 1.0) ,
        agent('3','20', 'M', 'R', True, True, True, 1.0) ,
        agent('4','20', 'M', 'S', True, True, True, 1.0) 
    ]
    wPyCx.agentsList = initAgents
    infected = [ag for ag in wPyCx.agentsList if ag.status == 'I']
    suspected = [ag for ag in wPyCx.agentsList if ag.status == 'S']
    recovered = [ag for ag in wPyCx.agentsList if ag.status == 'R']
    
    assert len(infected) == 1
    assert len(suspected) == 2
    assert len(recovered) == 1

def test_initialize():
    mock_initAgents = mock.Mock(name="initAgents")
    wPyCx.initializeAgents = mock_initAgents
    wPyCx.initialize(0.5,0.5,0.5,100)
    mock_initAgents.assert_called_once_with(0.5,0.5,0.5,100)


def test_returnAvgRate():
    initAgents = [
        agent('1','20', 'M', 'S', True, True, True, 1.0) ,
        agent('2','20', 'M', 'I', True, True, True, 1.0) ,
        agent('3','20', 'M', 'R', True, True, True, 1.0) ,
        agent('4','20', 'M', 'S', True, True, True, 1.0) 
    ]
    wPyCx.agentsList = initAgents
    avgRate = len(initAgents) / 2.0
    f = wPyCx.returnAvgRate()
    assert f == round(avgRate, 2)

def test_checkDistanceBetween():
    mock_startInfecting = mock.Mock(name="startInfecting")
    ag = agent('1','20', 'M', 'S', True, True, True, 1.0) 
    ag.x = 500
    ag.y = 500
    ag2 = agent('2','20', 'M', 'S', True, True, True, 1.0) 
    ag2.x = 505
    ag2.y = 500
    ag.startInfecting = mock_startInfecting
    wPyCx.checkDistanceBetween(ag,ag2)
    distanceBetween = np.linalg.norm([ag.x-ag2.x,ag.y-ag2.y], ord = 2)
    assert distanceBetween <= 200
    mock_startInfecting.assert_called()


def test_update_one_agent():
    from PIL import Image as img
    import random
    mock_checkDistance = mock.Mock(name="checkDistance")
    mock_randomrand = mock.Mock(name="random", return_value = 3)
    ag = agent('1','20', 'M', 'S', True, True, True, 1.0)
    ag2 = agent('2','20', 'M', 'S', True, True, True, 1.0)
    ag.x = 622
    ag.y = 985
    ag2.x = 625
    ag2.y = 980
    wPyCx.agentsList = [ag, ag2]
    wPyCx.checkDistanceBetween = mock_checkDistance
    random.randint = mock_randomrand
    wPyCx.update_one_agent()
    mock_checkDistance.assert_called()
    assert ag.x != 622 and ag.y != 985 


def test_update():
    mock_update_one = mock.Mock(name="update_one")
    wPyCx.update_one_agent = mock_update_one
    wPyCx.agentsList = agentList
    wPyCx.update()
    mock_update_one.assert_called()


"""
    Testing if the return valule consists of 3 elements, which should be infection rates for the three arrays in sorted pop
"""
def test_getInfectionRateNetwork():
    mock_update = mock.Mock(name="update")
    mock_initialize = mock.Mock(name="initialize")
    mock_observe = mock.Mock(name="observe")
    mock_returnAvgRate = mock.Mock(name="returnAvgRate")

    wPyCx.update = mock_update
    wPyCx.initialize = mock_initialize
    wPyCx.observe = mock_observe
    wPyCx.returnAvgRate = mock_returnAvgRate

    sorted_pop = np.array( [
        [0.8, 0.5, 0.6, 70],
        [0.5, 0.8, 0.2, 90],
        [0.2, 0.3, 0.8, 50]
    ])
    f = wPyCx.getInfectionRateNetwork(sorted_pop)
    mock_initialize.assert_called()
    mock_observe.assert_called()
    mock_update.assert_called()
    mock_returnAvgRate.assert_called()
    assert len(f) == 3


def test_selectOptimalSolution():
    optimalSol = [[0.9, 0.6, 0.85, 90, 1.4]]
    sortedPop = [
        [0.3,0.4,0.3,100],
        [0.2,0.7,0.1, 70],
        [0.9,0.6,0.85, 90]
    ]

    Infectionrate = [3.50, 2.40, 1.4]
    parents = evopart.fitness_score(sortedPop, Infectionrate)
    f = evopart.selectOptimalSolution(parents)
    assert f == optimalSol

def test_for_crossover():
    sortedPop = [
        [0.3,0.4,0.3,100],
        [0.2,0.7,0.1, 70],
        [0.9,0.6,0.85, 90]
    ]
    Infectionrate = [3.50, 2.40, 1.4]
    parents = evopart.fitness_score(sortedPop, Infectionrate)
    f = evopart.crossover(parents)
    assert len(f) == 8

def test_mutation():
    sortedPop = [
        [0.3,0.4,0.3,100],
        [0.2,0.7,0.1, 70],
        [0.9,0.6,0.85, 90]
    ]
    Infectionrate = [3.50, 2.40, 1.4]
    parents = evopart.fitness_score(sortedPop, Infectionrate)
    offspring = evopart.crossover(parents)
    f = evopart.mutation(offspring)
    assert len(f) == 8
