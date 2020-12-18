############################################################################################
# import packages
############################################################################################

import random
import numpy as np
import matplotlib.pyplot as plt
import time
import string
import matplotlib.animation as animation

############################################################################################
# set up and parameters
############################################################################################

# list of characters available
character_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                  'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', ' ']

# create secret password
secret_password = list("NhomDemo123")

# passcode length
password_length = len(secret_password)

# the number chromosomes that will be in the population
population_size = 100

# number of parents selected from the population each iteration
num_parents = 20

# number of the population that will be kept as is
elite_size = 2

############################################################################################
# create initial population set
############################################################################################

population = []
for i in range(population_size):

    chromosome = []
    for x in range(password_length):
        chromosome.append(random.choice(character_list))

    population.append(chromosome)

############################################################################################
# evolutionary functions
############################################################################################

# fitness scoring


def fitness(population):
    fitness_scores = []
    for chromosome in population:
        matches = 0
        for index in range(password_length):
            if secret_password[index] == chromosome[index]:
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

    geneA = int(random.random() * password_length)
    geneB = int(random.random() * password_length)

    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(0, password_length):
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
            mutated_position = int(random.random() * password_length)
            mutation = random.choice(character_list)
            children_set[i][mutated_position] = mutation
    return children_set


############################################################################################
# run GA
############################################################################################
fitness_tracker = []
solutions = []
generations = 0
t0 = time.time()
while True:

    fitness_scores = fitness(population)
    fitness_tracker.append(max([i[1] for i in fitness_scores]))
    solutions.append(''.join([i[0] for i in fitness_scores if i[1] == max(
        [i[1] for i in fitness_scores])][0]))
    print(''.join([i[0] for i in fitness_scores if i[1]
                   == max([i[1] for i in fitness_scores])][0]))
    if max([i[1] for i in fitness_scores]) == password_length:
        print("Cracked in {} generations, and {} seconds! \nSecret passcode = {} \nDiscovered passcode = {}".format(
            generations, time.time() - t0, ''.join(secret_password), ''.join([i[0] for i in fitness_scores if i[1] == password_length][0])))
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

x = list(range(len(solutions)))
y = list(range(len(solutions)))


def update_line(num, data, line):
    line.set_data(data[..., :num])
    solution_text.set_text(solutions[num])
    secret_password_str = "".join(secret_password)
    generation_text.set_text(
        "Passcode: {} -- Generation: {}" .format(secret_password_str, num))
    return line,


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
    solutions) + 1, fargs=(data, l), interval=20, repeat_delay=400)
plt.show()
