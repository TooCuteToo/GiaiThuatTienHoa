from tkinter import *
import numpy as np
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  
NavigationToolbar2Tk) 
import time
import random
import matplotlib.animation as animation
from functools import partial

############################################################################################
# set up and parameters
############################################################################################

# list of characters available
character_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I',
                  'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', '!', '"', '#', '$', '%', '&', "'", '(', ')', '*', '+', ',', '-', '.', '/', ':', ';', '<', '=', '>', '?', '@', '[', ']', '^', '_', '`', '{', '|', '}', '~', ' ']

# the number chromosomes that will be in the population
population_size = 100

# number of parents selected from the population each iteration
num_parents = 20

# number of the population that will be kept as is
elite_size = 2

############################################################################################
# create initial population set
############################################################################################

def initPopulation(password_length, population): 
  for i in range(population_size):

    chromosome = []
    for x in range(password_length):
        chromosome.append(random.choice(character_list))

    population.append(chromosome)
  return population

############################################################################################
# evolutionary functions
############################################################################################

# fitness scoring


def fitness(population, secret_password, password_length):
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


def breed(parents, parent1, parent2, password_length):
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


def create_children(parents_pool, population, password_length):
    children = []
    num_new_children = len(population) - elite_size

    for i in range(0, elite_size):
        children.append(parents_pool[i])

    for i in range(0, num_new_children):
        parent1 = parents_pool[int(random.random() * len(parents_pool))]
        parent2 = parents_pool[int(random.random() * len(parents_pool))]
        children.append(breed(parents_pool, parent1, parent2, password_length))
    return children

# mutation


def mutation(children_set, password_length):
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


def GA(population, generations, fitness_tracker, solutions, t0, secret_password, password_length):
  while True:
    fitness_scores = fitness(population, secret_password, password_length)
    fitness_tracker.append(max([i[1] for i in fitness_scores]))
    solutions.append(''.join([i[0] for i in fitness_scores if i[1] == max(
        [i[1] for i in fitness_scores])][0]))
    if max([i[1] for i in fitness_scores]) == password_length:
        break
    parents = select_parents(fitness_scores)
    children = create_children(parents, population, password_length)
    population = mutation(children, password_length)
    generations += 1
  
  return generations, fitness_tracker

root = Tk()

frame1 = Frame(root)
frame1.pack()

label = Label(frame1, text = "Enter a passcode: ")
label.grid(row = 0, column = 0, padx = (10, 5))

input = Entry(frame1, width = 50)
input.grid(row = 0, column = 1, padx = (0, 20), pady = 10)

def myClick():
  population = []
  fitness_tracker = []
  solutions = []
  generations = 0
  t0 = time.time()

  secret_password = list(input.get())
  password_length = len(secret_password)

  population = initPopulation(password_length, population)

  generations, fitness_tracker = GA(
    population, 
    generations, 

    fitness_tracker, 
    solutions, 

    t0, 
    secret_password, 

    password_length
  )

  plot(generations, fitness_tracker)
  animatedPlot(solutions, secret_password, fitness_tracker)

def plot(generations, fitness_tracker):
  fig = Figure(figsize = (5, 5), dpi = 100)
  fig.suptitle('Fitness Score by Generation', fontsize=14, fontweight='bold')

  plot1 = fig.add_subplot(111)
  plot1.plot(list(range(generations+1)), fitness_tracker)

  plot1.set_xlabel('Generation')
  plot1.set_ylabel('Fitness Score')

  # creating the Tkinter canvas 
  # containing the Matplotlib figure 
  canvas = FigureCanvasTkAgg(fig, frame3)   
  canvas.draw() 

  # placing the canvas on the Tkinter window 
  canvas.get_tk_widget().grid(row = 0, column = 0)

def animatedPlot(solutions, secret_password, fitness_tracker):
  x = list(range(len(solutions)))
  y = list(range(len(solutions)))
  
  data = np.array([x, y])
  fig = Figure(figsize = (12, 5), dpi = 100)

  plot1, ax = fig.subplots(2, 1)
  plot1.set_facecolor("black")

  ax.set_facecolor("black")
  fig.patch.set_facecolor("black")

  l, = plot1.plot([], [], 'r-', color="black")

  canvas = FigureCanvasTkAgg(fig, frame3)   
  canvas.get_tk_widget().grid(row = 0, column = 1)
  
  ax.set_xlim(0, 9000)
  ax.set_ylim(0, 150)

  ax.set_yticklabels([])
  ax.set_xticklabels([])

  ax.tick_params(axis=u'both', which=u'both', length=0)
  solution_text = ax.text(2500, 100, "", fontsize=20, color="white",
                          horizontalalignment='center', verticalalignment='center')

  generation_text = ax.text(0, 170, "", fontsize=20, color="white")

  global line_ani

  line_ani = animation.FuncAnimation(
    fig, 
    update_line, 
    
    len(solutions) + 1, 
    fargs=(data, l, solutions, secret_password, solution_text, generation_text, fitness_tracker), 

    interval=50, 
    repeat_delay=400
  )

    # placing the canvas on the Tkinter window 

def update_line(num, data, line, solutions, secret_password, solution_text, generation_text, fitness_tracker):
  line.set_data(data[..., :num])
  solution_text.set_text("Solution: {} --- Score: {}".format(solutions[num], fitness_tracker[num]))

  secret_password_str = "".join(secret_password)
  generation_text.set_text("Password: {} -- Generation: {}" .format(secret_password_str, num))

  return line,  

frame2 = Frame(root)
frame2.pack()

button = Button(text = "RUN", width = 20, command = myClick)
button.pack(pady = 10)

frame3 = Frame(root)
frame3.pack()

root.mainloop()



