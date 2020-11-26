import pytest
import numpy as np
# import Evopart
import random

@pytest.fixture(autouse=True)
def selectOptimalSolution():
    parents = 0
    optimal_solution = []
    # parents = np.array(parents)
    #
    # min_infection_parent = parents[parents[:, 4].argsort()]
    # min_infection_parent = min_infection_parent[0:1, :]
    # min_infection_parent = min_infection_parent[0].tolist()
    # if len(optimal_solution) == 0:
    #     optimal_solution.append(min_infection_parent)
    # else:
    #     if optimal_solution[0][4] > min_infection_parent[4]:
    #         optimal_solution.pop()
    #         optimal_solution.append(min_infection_parent)
    # print("The optimal Solution is:", optimal_solution)
    return [optimal_solution]


def test_for_selectOptimalSolution(selectOptimalSolution):

    O_S = []

    parents = np.array(selectOptimalSolution)
    # min_infection_parent = parents[parents[:, 4].argsort()]
    # min_infection_parent = min_infection_parent[0:1, :]
    # min_infection_parent = min_infection_parent[0].tolist()
    # if len(O_S) == 0:
    #     O_S.append(min_infection_parent)
    # else:
    #     if O_S[0][4] > min_infection_parent[4]:
    #         O_S.pop()
    #         O_S.append(min_infection_parent)

    assert selectOptimalSolution[0] == O_S


@pytest.fixture(autouse=True)
def crossover():
    parents = 0
    parents = np.array(parents)
    parents = np.delete(parents, 4, axis=1)
    split = 1
    # parent1_old = parents[:split, :]  # making the 2d array to 2 1d array
    # parent2_old = parents[split:, :]
    # for i in parent1_old:
    #     parent1 = np.array(i)
    # for i in parent2_old:
    #     parent2 = np.array(i)

    offsprings = []
    x = 2
    y = 1
    z = 3
    k = 4  # the parents will come
    #
    # offspring_1 = np.append(parent1[:x], parent2[x:])
    # offspring_2 = np.append(parent2[:x], parent1[x:])
    # offspring_3 = np.append(parent1[:y], parent2[y:])
    # offspring_4 = np.append(parent2[:y], parent1[y:])
    # offspring_5 = np.append(parent1[:z], parent2[z:])
    # offspring_6 = np.append(parent2[:z], parent1[z:])
    # offspring_7 = np.append(parent1[:k], parent2[k:])
    # offspring_8 = np.append(parent2[:k], parent1[k:])
    # offsprings = np.append(offsprings,
    #                        [offspring_1, offspring_2,
    #                         offspring_3, offspring_4,
    #                         offspring_5, offspring_6,
    #                         offspring_7, offspring_8])
    # offsprings = offsprings.reshape(-1, 4)
    # print("After crossover: ")
    # print(np.array_str(offsprings, precision=2, suppress_small=True))
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
    # mutated_offsprings[:, [start_index, last_index]] = mutated_offsprings[:, [last_index, start_index]]
    for i in mutated_offsprings:
        i[3] = (random.randint(20, 180))
    # print("After mutation: It is swaping betn the 1st&3rd column and changing the last column")
    # print(np.array_str(mutated_offsprings, precision=2, suppress_small=True))
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



