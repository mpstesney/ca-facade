"""
Coursework for Generative Systems for Design, Fall 2019,
Carnegie Mellon University

Author: Michael Stesney mstesney@andrew.cmu.edu

Cellular automata driven building facade active shading device

"""


import Rhino.Geometry as rg
import random
import math

class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.cells = self.createCells() # list of cells
        self.setState()
        self.radiation = [0.0] * len(self.cells) # initial state
        self.setCombustibility()
        self.setOpenness()
        self.assignNeighbors()

    def createCells(self):
        new_cells = []
        for y in range(self.height):
            for x in range(self.width):
                cell = Cell(x,y)
                cell.index = y*self.width + x
                new_cells.append(cell)
        return new_cells

    def setState(self): # 75% open at inititiation
        for cell in self.cells:
            n = random.random()
            if n < 0.25:
                cell.state = 0
            else:
                cell.state = 1

    def setCombustibility(self): # 
        comb_max = 1.0
        comb_min = 0.5
        for i in range(len(self.cells)):
            r = self.radiation[i]
            self.cells[i].combustibility = r*(comb_max - comb_min) + comb_min

    def setOpenness(self):
        for cell in self.cells:
            cell.openness = ((cell.state + 1) % 3) / 2

    def assignNeighbors(self): # periodic edges. makes sense for base and head?
        for i in range(len(self.cells)):
            neighbors = []
            t = [(-1, 1), (0, 1), (1, 1), (-1, 0), (0, 0), (1, 0), (-1, -1), (0, -1), (1, -1)]
            for j in range(9):
                    nx = self.cells[i].x + t[j][0]
                    if nx < 0: nx = self.width - 1
                    if nx > self.width -1: nx = 0
                    ny = self.cells[i].y + t[j][1]
                    if ny < 0: ny = self.height - 1
                    if ny > self.height - 1: ny = 0
                    neighbors.append(self.cells[ny*self.width + nx])
            neighbors[4] = None
            self.cells[i].neighbors = neighbors

    def sumNeighborsOnFire(self):
        for cell in self.cells:
            sum = 0
            for neighbor in cell.neighbors:
                if neighbor != None and neighbor.state == 2:
                    sum += 1
            cell.neighborsSumOnFire = sum

    def updateRadiation(self, hour): # data from lady bug
        h = hour % 24
        vals = sun_data[h]
        for i in range(len(vals)):
            self.radiation[i] = vals[i]
            

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.index = 0
        self.state = 0
        self.state_prev = self.state
        self.neighbors = [] # list of cells
        self.neighborsSumOnFire = 0
        self.combustibility = 0
        self.counter = 0
        self.isEasing = False
        self.ease_val = 1
        self.counter2 = 0
        self.isOpening = False
        self.isClosing = False
        self.openness = 0
        self.openness_prev = self.openness
    
    def __repr__(self):
        return "({}, {}, {})".format(self.index, self.state, self.neighborsSumOnFire)
    
    def updateStateGrowth(self):
        r = random.random()
        self.state_prev = self.state
        self.openness_prev = self.openness
        if r < P1:
            self.state = 1
            self.openness = 1

    def updateStateLightning(self):
        r1 = random.random()
        r2 = random.random()
        self.state_prev = self.state
        self.openness_prev = self.openness
        if r1 < P2l and r2 < self.combustibility:
            self.state = 2
            self.openness = 0
    
    def updateStateFire(self):
        r1 = random.random()
        r2 = random.random()
        self.state_prev = self.state
        self.openness_prev = self.openness
        if r1 < P2a and r2 < self.combustibility:
            self.state = 2

    def updateStateExt(self):
        r1 = random.random()
        r2 = random.random()
        self.state_prev = self.state
        self.openness_prev = self.openness
        if r1 < P3 and r2 > self.combustibility:
            self.state = 0
            self.openness = 0.5

    def ease(self): # delay needs to be at least 10 to work properly
        self.counter += 1
        step = delay/10
        self.ease_val = (self.counter * step) / delay
        if self.counter * step == delay:
            self.ease_val = 1
            self.isEasing = False
            self.counter = 0

    def open(self): # delay needs to be at least 10 to work properly
        self.counter2 += 1
        step = delay/10
        i =  (self.counter2 * step) / delay
        self.openness = self.openness_prev + (i/2)
        if self.counter2 * step == delay:
            self.openness = self.openness_prev + 0.5
            self.isOpening = False
            self.counter2 = 0

    def close(self): # delay needs to be at least 10 to work properly
        self.counter2 += 1
        step = delay/10
        self.openness = 1 - ((self.counter2 * step) / delay)
        if self.counter2 * step == delay:
            self.openness = 0 
            self.isClosing = False
            self.counter2 = 0

######

# 1 initialize map

if reset:
    random.seed(seed)
    map = Map(width, height)
    counter = 0
    hour = 0

# 2 iterate over generations

else:
    counter += 1
    
    # update solar radiation values
    if counter % (delay*10) == 0:
        map.updateRadiation(hour)
        map.setCombustibility()
        hour += 1
    
    #update states
    if counter % delay == 0: # delay update to allow for easing
        map.sumNeighborsOnFire()
        for cell in map.cells:
            if cell.state == 0:
                cell.updateStateGrowth()
                if cell.state != cell.state_prev:
                    cell.isEasing = True
                    cell.isOpening = True
            elif cell.state == 1:
                cell.updateStateLightning()
                if cell.neighborsSumOnFire > 0:
                    cell.updateStateFire()
                if cell.state != cell.state_prev:
                    cell.isEasing = True
                    cell.isClosing = True
            else:
                cell.updateStateExt()
                if cell.state != cell.state_prev:
                    cell.isEasing = True
                    cell.isOpening = True
    
    # move sunshades, adjust opacity, etc
    for cell in map.cells:
        if cell.isEasing == True:
            cell.ease()
        if cell.isOpening == True:
            cell.open()
        if cell.isClosing == True:
            cell.close()

# 3 output

a = [cell.state for cell in map.cells]
b = [cell.openness for cell in map.cells]
c = [cell.combustibility for cell in map.cells]

empty = 0
alive = 0
onfire = 0
for cell in map.cells:
    if cell.state == 0: empty += 1
    elif cell.state == 1: alive += 1
    else: onfire += 1
per_empty = empty/len(map.cells)*100
per_alive = alive/len(map.cells)*100
per_onfire = onfire/len(map.cells)*100


open_per = (((empty*0.5) + (alive*1.0)) / len(map.cells))*100

d = "states:\n{:0.1f}% empty\n{:0.1f}% alive\n{:0.1f}% on fire".format(per_empty, per_alive, per_onfire)
e = "probabilities:\n{:0.4f} empty to alive\n{:0.4f} lightning\n{:0.4f} fire spread\n{:0.4f} extinguish".format(P1, P2l, P2a, P3)
f = "{:0.2f} solar radiation\n{:0.2f} combustibility".format(map.radiation[200], map.cells[200].combustibility)
g = "performance:\n{:02d} o'clock\n{:0.2f} % area open".format(hour, open_per)
