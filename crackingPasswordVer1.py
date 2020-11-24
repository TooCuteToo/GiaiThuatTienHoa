############################################################################################
# import packages
############################################################################################

import random
import numpy as np
import matplotlib.pyplot as plt
import time
import matplotlib.animation as animation

############################################################################################
# set up and parameters
############################################################################################

# passcode length
passcode_length = 8

# min number
passcode_lower_bound = 0

# max number
passcode_upper_bound = 9

# the number chromosomes that will be in the population
population_size = 10

# number of parents selected from the population each iteration
num_parents = 5

# number of the population that will be kept as is
elite_size = 2

# create secret password
secret_passcode = []
for x in range(passcode_length):
    secret_passcode.append(
        int(round(random.uniform(passcode_lower_bound, passcode_upper_bound), 0)))

print(secret_passcode)

############################################################################################
# create initial population set
############################################################################################

population = []
for i in range(population_size):
    chromosome = []
    for x in range(passcode_length):
        chromosome.append(
            int(round(random.uniform(passcode_lower_bound, passcode_upper_bound), 0)))
    population.append(chromosome)

############################################################################################
# evolutionary functions
############################################################################################

# fitness scoring


def fitness(population):
    fitness_scores = []
    for chromosome in population:
        matches = 0
        for index in range(passcode_length):
            if secret_passcode[index] == chromosome[index]:
                matches += 1
        result = [chromosome, matches]
        fitness_scores.append(result)
    return fitness_scores

# parent selection


def select_parents(fitness_scores):
    parents_list = []
    for chromosome in sorted(fitness_scores, key=lambda x: x[1], reverse=True)[:num_parents]:
        parents_list.append(chromosome[0])
    return(parents_list)

# breeding logic


def breed(parent1, parent2):
    child = []

    parent1 = parents[0]
    parent2 = parents[1]

    geneA = int(random.random() * passcode_length)
    geneB = int(random.random() * passcode_length)

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(0, passcode_length):
        if (i < startGene) or (i > endGene):
            child.append(parent1[i])
        else:
            child.append(parent2[i])
    return child

# breeding and elitism


def create_children(parents_pool):
    children = []
    num_new_children = len(population) - elite_size

    for i in range(0, elite_size):
        children.append(parents_pool[i])

    for i in range(0, num_new_children):
        parent1 = parents_pool[int(random.random() * len(parents_pool))]
        parent2 = parents_pool[int(random.random() * len(parents_pool))]
        children.append(breed(parent1, parent2))
    return children

# mutation


def mutation(children_set):
    for i in range(len(children_set)):
        if random.random() > 0.1:
            continue
        else:
            mutated_position = int(random.random() * passcode_length)
            mutation = int(round(random.uniform(
                passcode_lower_bound, passcode_upper_bound+1), 0))
            children_set[i][mutated_position] = mutation
    return children_set


############################################################################################
# run GA
############################################################################################
success = []
fitness_tracker = []
generations = 0
t0 = time.time()
while True:

    fitness_scores = fitness(population)
    fitness_tracker.append(max([i[1] for i in fitness_scores]))
    success.append([i[0] for i in fitness_scores if i[1] == max(
        [i[1] for i in fitness_scores])][0])
    if max([i[1] for i in fitness_scores]) == passcode_length:
        print("Cracked in {} generations, and {} seconds! \nSecret passcode = {} \nDiscovered passcode = {}".format(
            generations, time.time() - t0, secret_passcode, [i[0] for i in fitness_scores if i[1] == passcode_length][0]))
        break
    parents = select_parents(fitness_scores)
    children = create_children(parents)
    population = mutation(children)
    generations += 1

############################################################################################
# plot max fitness per generation
############################################################################################

fig = plt.figure()
plt.plot(list(range(generations+1)), fitness_tracker)
fig.suptitle('Fitness Score by Generation', fontsize=14, fontweight='bold')
ax = fig.add_subplot(111)
ax.set_xlabel('Generation')
ax.set_ylabel('Fitness Score')
plt.show()

############################################################################################
# animated plot
############################################################################################

x = list(range(len(success)))
y = list(range(len(success)))


def update_line(num, data, line):
    line.set_data(data[..., :num])
    solution_text.set_text(success[num])
    secret_passcode_str = "".join(map(str, secret_passcode))
    generation_text.set_text(
        "Passcode: {} -- Generation: {}" .format(secret_passcode_str, num))
    return line


fig, ax = plt.subplots(figsize=(12, 6))
data = np.array([x, y])

ax.set_facecolor("black")
fig.patch.set_facecolor('black')
l, = plt.plot([], [], 'r-', color="black")
ax.set_xlim(0, 7000)
ax.set_ylim(0, 200)
ax.set_yticklabels([])
ax.set_xticklabels([])
ax.tick_params(axis=u'both', which=u'both', length=0)
solution_text = ax.text(3500, 100, "", fontsize=30, color="white",
                        horizontalalignment='center', verticalalignment='center')
generation_text = ax.text(100, 170, "", fontsize=20, color="white")
line_ani = animation.FuncAnimation(fig, update_line, len(
    success) + 1, fargs=(data, l), interval=20, repeat_delay=400)
plt.show()
