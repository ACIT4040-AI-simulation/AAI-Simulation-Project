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

