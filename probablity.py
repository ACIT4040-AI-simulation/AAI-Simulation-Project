#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 01:27:49 2020

@author: kassahundegena
"""

from numpy.random import choice
#import random
#sampleNumbers = []
choicelist = [True, False]
# Numpy's random.choice() to choose elements with different probabilities
#sampleNumbers = choice(numberList, 1, p=[0.75, 0.25])
totalcount =0
for j in range(10):
    count = 0
    sampleNumbers = []
    for i in range(10):
        #sample=random.choices([True, False], cum_weights=(75, 25), k=1)
        sample = choice([True, False], 1, p=[0.75, 0.25])

        #print(sample)
        sampleNumbers.append(sample[0])
        if sample[0]:
            count = count + 1
        
    print("count = ", count ,"List = ", sampleNumbers)
    totalcount = totalcount + count
print("probablity of true= ", totalcount/100)

#print(range(5))

class test:
    val = 5
    friend = ''
    def calc(self, a):
        a.calc(self)
    def mkfriend(self, ag):
        friend = ag

x = test()
