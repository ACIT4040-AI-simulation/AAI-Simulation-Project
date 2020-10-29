import pycxsimulator
from pylab import *

populationSize = 100
noiseLevel = 1

class agent():
    def __init__(self,x,y):
        self.x = x
        self.y = y

def initialize():
    global time, agents

    time = 0

    agents = []
    for i in range(populationSize):
        newAgent = agent(random(),random())
        agents.append(newAgent)

def observe():
    cla()   
    x = [ag.x for ag in agents]
    y = [ag.y for ag in agents]
    plot(x, y, 'bo', alpha = 0.2)
    axis('scaled')
    axis([-100, 100, -100, 100])
    title('t = ' + str(time))

def update():
    global time, agents

    time += 1

    for ag in agents:
        ag.x =  (ag.x + noiseLevel) if (ag.x + noiseLevel) <= 100 else 100-(ag.x + noiseLevel)
       # ag.y +=  noiseLevel

pycxsimulator.GUI().start(func=[initialize, observe, update])
            