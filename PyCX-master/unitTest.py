import os
from os import name
import numpy as np
import pytest
import unittest
from unittest import mock
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
