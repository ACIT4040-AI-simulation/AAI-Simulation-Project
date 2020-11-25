import pytest
# from PyCX-master import evo_agent.py

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

import os

import WithoutPyCx as wPyCx
from evo_agent import evo_agent as agent


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

"""
Testing the changePercentageOfInfectedAgents checking the number of infected people in a list of 3 people, when infection rate is 80%, expected result:2
"""
def test_changePercentageOfInfectedAgents():
    agentObjList = []
    infectedList = []

    for agentObj in agentList:
        temp = agent(agentObj['id_no'], agentObj['age'], agentObj['gender'], agentObj['status'], agentObj['mask'],
                     agentObj['antibact'], agentObj['socialDistance'], agentObj['infectionRate'])
        agentObjList.append(temp)
    f =   wPyCx.changePercentageOfInfectedAgents(0.8, agentObjList)
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

##This a random generator function, dont know how to test randomness
#def test_random_array_generator():

#def test_sorted_population():

