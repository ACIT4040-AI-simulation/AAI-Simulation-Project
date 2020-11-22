#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 30 12:26:27 2020

@author: emanazab
"""

import networkx as nx
import numpy as np
from pylab import *

populationSize = 30
linkProbability = 0.3
initialInfectedRatio = 0.4
recoveryProb = 0.4

infectionRateList=[]


MaskBool=False
HandSaniBool=False
SocialDistanceBool=False
SharedObjectBool=False


susceptible = 'gray'
infected = 'r'
recovered = 'g'


def initialize(MaskProb,HandSaniProb,SocialDistanceProb,SharedObjectProb):
    global time, network, positions, nextNetwork
    
    time = 0
    
    network = nx.binomial_graph(populationSize, linkProbability)

    positions = nx.spring_layout(network)

    initializeRandomNodeStatus(network)
    maskStatus(network,MaskProb)
    handSaniStatus(network,HandSaniProb)
    socialDistanceStatus(network,SocialDistanceProb)
    #call sharedObjectStatus function
    sharedObjectStatus(network,SharedObjectProb)
    nextNetwork = network.copy()
    
    
def observe():
    
    cla()
   
    nx.draw(network,
            pos = positions,
            node_color = [network.nodes[i]['state'] for i in network.nodes],
            node_size=80,
           )
    axis('image')
 
   
    title('t = ' + str(time))
    
def update(isolation_prob):
    global time, network, nextNetwork

    time += 1
    
    for i in network.nodes:
         if network.nodes[i]['state'] == susceptible:
            #check only the next node to the current node
            for j in network.neighbors(i):
                if network.nodes[i]['state'] == susceptible and network.nodes[j]['state'] == infected:
                    infectionRate(network.nodes[i], network.nodes[j])
                #decide wether if greater than or less than 
                if network.nodes[i]['infectionRate']> random():
                    #print(network.nodes[i]['infectionRate'], random())
                    nextNetwork.nodes[i]['state'] = infected
                    list(nextNetwork.nodes[i])
                    nextNetwork.nodes[i]['infectionRate']=0
                    break 
                #decide wether if greater than or less than 
                elif network.nodes[i]['infectionRate']< isolation_prob:
                    if nextNetwork.has_edge(i, j):
                                nextNetwork.remove_edge(i, j)
                    
         elif network.nodes[i]['state'] == infected:
            if random() < recoveryProb :
                nextNetwork.nodes[i]['state'] = recovered
            for j in network.neighbors(i):
                if network.nodes[j]['state'] == susceptible:
                    infectionRate(network.nodes[i], network.nodes[j])
                    #decide wether if greater than or less than 
                    if network.nodes[i]['infectionRate']> random():
                        nextNetwork.nodes[i]['state'] = infected
                        list(nextNetwork.nodes[i])
                        nextNetwork.nodes[i]['infectionRate']=0
                        break
                    elif network.nodes[i]['infectionRate']< isolation_prob:
                        if nextNetwork.has_edge(i, j):
                                nextNetwork.remove_edge(i, j)
    del network
    network = nextNetwork.copy()
    
#Generate random nodes status
def initializeRandomNodeStatus(network):
    for i in network.nodes:
        if random() < initialInfectedRatio:
            network.nodes[i]['state'] = infected 
        else:
            network.nodes[i]['state'] = susceptible
        network.nodes[i]['infectionRate'] = float(0)
        
#Generate random nodes with different Maskbool values
def maskStatus(network,MaskProb):
    for i in network.nodes:
        if random() < MaskProb:
            network.nodes[i]['Maskbool'] = True 
        else:
            network.nodes[i]['Maskbool'] = False
            
 #Generate random nodes with different HandSanibool values           
def handSaniStatus(network,HandSaniProb):
    for i in network.nodes:   
        if random() < HandSaniProb :
            network.nodes[i]['HandSanibool'] = True 
        else:
            network.nodes[i]['HandSanibool'] = False
            
#Generate random nodes with different SocialDistancebool values
def socialDistanceStatus(network,SocialDistanceProb):
    for i in network.nodes:   
        if random() < SocialDistanceProb :
            network.nodes[i]['socialDistancebool'] = True 
        else:
            network.nodes[i]['socialDistancebool'] = False
         
#Generate random nodes with different sharedObjectbool values
def sharedObjectStatus(network,SharedObjectProb):
    for i in network.nodes:   
        if random() < SharedObjectProb :
            network.nodes[i]['SharedObjectBool'] = True 
        else:
            network.nodes[i]['SharedObjectBool'] = False

#calculate the infection rate for susceptible nodes with infected neighbours node
def infectionRate(currentNode, neighbourNode):
    #if the current node infected and the neighbour is susceptible
    if currentNode['state'] == infected:
        if currentNode['Maskbool']== True:
            if neighbourNode['Maskbool'] == True:
                list(neighbourNode)
                neighbourNode['infectionRate'] = 0.015
            elif neighbourNode['Maskbool']!= True:
                list(neighbourNode)
                neighbourNode['infectionRate'] = 0.05
        elif currentNode['Maskbool']!= True:
            list(neighbourNode)
            neighbourNode['infectionRate'] = 0.7
        
        #check if the current node applying HandSani
        if neighbourNode['HandSanibool'] == True:
            neighbourNode['infectionRate'] = neighbourNode['infectionRate'] * 0.16
        
        #check if the neighbour node applying socialDistance
        if neighbourNode['socialDistancebool']== True:
            neighbourNode['infectionRate'] = neighbourNode['infectionRate'] * 0.40
        
        #check if the neighbour node using sharedobjects
        if neighbourNode['SharedObjectBool']== True:
            neighbourNode['infectionRate'] = neighbourNode['infectionRate'] * 0.60
            
        if neighbourNode['infectionRate']>0:
            infectionRateList.append(neighbourNode['infectionRate'])
        
    #if the current node susceptible and the neighbour is infected    
    elif currentNode['state'] == susceptible:
        if neighbourNode['Maskbool']== True:
            if currentNode['Maskbool']== True:
                list(currentNode)
                currentNode['infectionRate'] = 0.015
            elif currentNode['Maskbool']!= True:
                list(currentNode)
                currentNode['infectionRate'] = 0.05
        elif neighbourNode['Maskbool']!= True:
            list(currentNode)
            currentNode['infectionRate'] = 0.7
        
        #check if the current node applying HandSani
        if currentNode['HandSanibool'] == True:
           currentNode['infectionRate'] = currentNode['infectionRate'] * 0.16
        
        #check if the current node applying socialDistance
        if currentNode['socialDistancebool']:
           currentNode['infectionRate'] = currentNode['infectionRate'] * 0.40
        
         #check if the current node using sharedobjects
        if currentNode['SharedObjectBool']:
           currentNode['infectionRate'] = currentNode['infectionRate'] * 0.60
        
        if currentNode['infectionRate']>0:
            infectionRateList.append(currentNode['infectionRate'])

def getInfectionRateNetwork(sorted_pop):
    totalInfectionRate=[]
    sorted_pop_arr = sorted_pop.tolist()
    for i in range(len(sorted_pop_arr)):
        initialize(sorted_pop_arr[i][0],sorted_pop_arr[i][1],sorted_pop_arr[i][2],sorted_pop_arr[i][3])
        observe()
        update(sorted_pop_arr[i][4])
        totalInfectionRate.append(round(sum(infectionRateList),2))
        infectionRateList.clear()
    return totalInfectionRate

