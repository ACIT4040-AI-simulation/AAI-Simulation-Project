from unittest import mock
import os
import numpy as np
import pytest
import WithoutPyCx as wPyCx
import Evopart as evopart
import random


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


@pytest.fixture(autouse=True)
def crossover():
    parents = 0
    parents = np.array(parents)
    parents = np.delete(parents, 4, axis=1)
    split = 1
    offsprings = []
    x = 2
    y = 1
    z = 3
    k = 4
    
    return [parents,
            split,
            x,
            y,
            z,
            k,
            offsprings]


def test_for_crossover(crossover):
    offsprings = []
    parent1_old = 0
    parent2_old = 0
    paretnts = 0
    split = 1
    x = 2
    y = 1
    z = 3
    k = 4

    assert crossover[0] == paretnts
    assert crossover[1] == split
    assert crossover[2] == x
    assert crossover[3] == y
    assert crossover[4] == z
    assert crossover[5] == k



@pytest.fixture(autouse=True)
def mutation():  # does swaping within 1st and 3rd column also randomly changes the last column which is agents within the range 20 to 180
    start_index = 0  # swaping points
    last_index = 2
    mutated_offsprings = []
    for i in mutated_offsprings:
        i[3] = (random.randint(20, 180))
    return [start_index,
            last_index,
            mutated_offsprings]

def test_for_mutation(mutation):

    start_index = 0
    last_index = 2
    mutated_offsprings = []
    for i in mutated_offsprings:
         i[3] = (random.randint(20, 180))
    assert mutation[0] == start_index
    assert mutation[1] == last_index
    assert mutation[2] == mutated_offsprings



