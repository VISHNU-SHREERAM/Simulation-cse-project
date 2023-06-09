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
    def __init__(self, age, x, y):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.x = x
        self.y = y

    def move(self):
        self.x += random.uniform(-0.01, 0.01)
        self.y += random.uniform(-0.01, 0.01)
        self.x = max(0, min(10, self.x))
        self.y = max(0, min(10, self.y))

class Lion:
    def __init__(self, age, skill, x, y):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.skill = skill
        self.health = 10
        self.x = x
        self.y = y

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
            if len(peopleDictionary) > 0 and len(peopleDictionary) / area > 1:
                start_index = int(random.randint(0, len(peopleDictionary) - 1))
                end_index = start_index + 1
                del peopleDictionary[start_index:end_index]
                if lion.health < 10 and lion.skill > 1:
                    lion.health += lion.skill
            else:
                lion.health -= 1
                if lion.health < 1:
                    LionDictionary.remove(lion)

def reproduce(fertilityx, fertilityy, infantMortality, LioninfantMortality):
    for person in peopleDictionary:
        if person.gender == 1 and fertilityx < person.age < fertilityy:
            if random.randint(0, 5) == 1 and random.randint(0, 100) > infantMortality:
                peopleDictionary.append(Person(0, person.x, person.y))
    for lion in LionDictionary:
        if lion.gender == 1 and fertilityx < lion.age < fertilityy:
                if random.randint(0, 3) == 1 and random.randint(0, 100) > LioninfantMortality:
                    ranskill = random.uniform(lion.skill - 0.5, lion.skill + 0.5)
                    LionDictionary.append(Lion(0, ranskill, lion.x, lion.y))

def beginSim():
    for _ in range(startPopulation):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        peopleDictionary.append(Person(random.randint(18, 50), x, y))
    for _ in range(startPopulation_Lion):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        LionDictionary.append(Lion(random.randint(18, 30), random.uniform(1, 2.5), x, y))

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
    if random.randint(0, 300)==50:
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)

        LionDictionary.append(Lion(10,4,x,y))
        LionDictionary.append(Lion(10,4,x,y))
        LionDictionary.append(Lion(10,4,x,y))
beginSim()

# Create a figure and axis
fig, ax = plt.subplots()

# Set the limits of the plot
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)

# Create scatter plots for people and lions
people_plot = ax.scatter([], [], c='blue', label='People')
lion_plot = ax.scatter([], [], c='red', label='Lions')

# Update function to be called for each frame
def update(frame):
    runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance, youthMortality, LioninfantMortality)
# Update the positions of people and lions
    people_x = [person.x for person in peopleDictionary]
    people_y = [person.y for person in peopleDictionary]
    lion_x = [lion.x for lion in LionDictionary]
    lion_y = [lion.y for lion in LionDictionary]
    for i, person in enumerate(peopleDictionary):
        dx = random.uniform(-0.1, 0.1)  # Random displacement in the x direction
        dy = random.uniform(-0.1, 0.1)  # Random displacement in the y direction
        people_x[i] += dx
        people_y[i] += dy

    for i, lion in enumerate(LionDictionary):
        dx = random.uniform(-0.00001, 0.000001)  # Random displacement in the x direction
        dy = random.uniform(-0.0001, 0.0001)  # Random displacement in the y direction
        lion_x[i] += dx
        lion_y[i] += dy

    # Update the scatter plots
    people_plot.set_offsets(np.column_stack((people_x, people_y)))
    lion_plot.set_offsets(np.column_stack((lion_x, lion_y)))

    # Update the plot labels
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    # Update the plot legend
    ax.legend()

# Create the animation
animation = FuncAnimation(fig, update, frames=range(100000), interval=1)

# Show the plot
plt.show()

