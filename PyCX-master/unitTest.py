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



