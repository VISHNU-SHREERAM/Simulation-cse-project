import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

startPopulation_Lion = 50
startPopulation = 3000
infantMortality = 10
LioninfantMortality = 0
youthMortality = 0
agriculture = 5
disasterChance = 10
fertilityx = 18
fertilityy = 40
food = 1
peopleDictionary = []
LionDictionary = []
area = 100
averageskill = 0

class Person:
    def __init__(self, age, x, y, range1):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.x = x
        self.y = y
        self.range = range1

    def move(self):
        self.x += random.uniform(-0.01, 0.01)
        self.y += random.uniform(-0.01, 0.01)
        self.x = max(0, min(10, self.x))
        self.y = max(0, min(10, self.y))

class Lion:
    def __init__(self, age, skill, x, y, range1):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.skill = skill
        self.health = 10
        self.x = x
        self.y = y
        self.range = range1

    def move(self):
        self.x += random.uniform(-0.5, 0.5)
        self.y += random.uniform(-0.5, 0.5)
        self.x = max(0, min(10, self.x))
        self.y = max(0, min(10, self.y))

def harvest(food, agriculture):
    ablePeople = 0
    for person in peopleDictionary:
        if person.age > 8:
            ablePeople += 1
    food += ablePeople * agriculture

    if food < len(peopleDictionary):
        del peopleDictionary[0:int(len(peopleDictionary) - food)]
        food = 0
    else:
        food -= len(peopleDictionary)

def avgskill():
    sum = 0
    for lion in LionDictionary:
        sum += lion.skill
    if len(LionDictionary) > 0:
        return sum / len(LionDictionary)
    else:
        return 0

def prey():
    for lion in LionDictionary:
        if lion.age > 8:
            preyInRange = [person for person in peopleDictionary if distance(person.x, person.y, lion.x, lion.y) <= lion.range]
            if preyInRange:
                if lion.health < 10 and lion.skill > 1:
                    lion.health += lion.skill
                    preyToRemove = random.choice(preyInRange)
                    peopleDictionary.remove(preyToRemove)
            else:
                lion.health -= 1
                if lion.health < 1:
                    LionDictionary.remove(lion)

def reproduce(fertilityx, fertilityy, infantMortality, LioninfantMortality):
    for person in peopleDictionary:
        if person.gender == 1 and fertilityx < person.age < fertilityy:
            potentialMates = [p for p in peopleDictionary if p.gender == 0 and distance(person.x, person.y, p.x, p.y) <= person.range]
            if potentialMates and random.randint(0, 5) == 1 and random.randint(0, 100) > infantMortality:
                mate = random.choice(potentialMates)
                peopleDictionary.append(Person(0, person.x, person.y, person.range))
    for lion in LionDictionary:
        if lion.gender == 1 and fertilityx < lion.age < fertilityy:
            potentialMates = [l for l in LionDictionary if l.gender == 0 and distance(lion.x, lion.y, l.x, l.y) <= lion.range]
            if potentialMates and random.randint(0, 3) == 1 and random.randint(0, 100) > LioninfantMortality:
                ranskill = random.uniform(lion.skill - 0.5, lion.skill + 0.5)
                mate = random.choice(potentialMates)
                LionDictionary.append(Lion(0, ranskill, lion.x, lion.y, lion.range))

def beginSim():
    for _ in range(startPopulation):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        range1 = random.uniform(1, 2)
        peopleDictionary.append(Person(random.randint(18, 50), x, y, range))
    for _ in range(startPopulation_Lion):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        range1 = random.uniform(1, 2)
        LionDictionary.append(Lion(random.randint(18, 30), random.uniform(1, 2.5), x, y, range))

def runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance, youthMortality, LioninfantMortality):
    harvest(food, agriculture)
    prey()

    for person in peopleDictionary:
        if person.age > 80:
            peopleDictionary.remove(person)
        else:
            person.age += 1
            person.move()

    for lion in LionDictionary:
        if lion.age > 50:
            LionDictionary.remove(lion)
        else:
            lion.age += 1
            lion.move()

    reproduce(fertilityx, fertilityy, infantMortality, LioninfantMortality)

    if random.randint(0, 100) < disasterChance:
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]

    infantMortality *= 0.985

    if random.randint(0, 100) < youthMortality:
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]

    youthMortality *= 0.9
    if random.randint(0, 300) == 50:
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        range1 = random.uniform(1, 2)

        LionDictionary.append(Lion(10, 4, x, y, range1))
        LionDictionary.append(Lion(10, 4, x, y, range1))
        LionDictionary.append(Lion(10, 4, x, y, range1))

def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

beginSim()

fig, ax = plt.subplots()
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

people_plot = ax.scatter([], [], c='blue', label='People')
lion_plot = ax.scatter([], [], c='red', label='Lions')

def init():
    # Initialize scatter plot data as empty arrays
    people_plot.set_offsets([])
    lion_plot.set_offsets([])
    return people_plot, lion_plot


def update(frame):
    runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance, youthMortality, LioninfantMortality)

    people_x = [person.x for person in peopleDictionary]
    people_y = [person.y for person in peopleDictionary]
    lion_x = [lion.x for lion in LionDictionary]
    lion_y = [lion.y for lion in LionDictionary]

    people_plot.set_offsets(np.c_[people_x, people_y])
    lion_plot.set_offsets(np.c_[lion_x, lion_y])

    return people_plot, lion_plot

ani = FuncAnimation(fig, update, frames=range(200), init_func=init, blit=True)
plt.legend()
plt.show()

