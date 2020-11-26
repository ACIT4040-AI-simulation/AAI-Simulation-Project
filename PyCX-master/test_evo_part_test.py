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


