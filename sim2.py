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
    def __init__(self, age, x, y, range_):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.x = x
        self.y = y
        self.range = range_

    def move(self):
        self.x += random.uniform(-0.01, 0.01)
        self.y += random.uniform(-0.01, 0.01)
        self.x = max(0, min(10, self.x))
        self.y = max(0, min(10, self.y))

class Lion:
    def __init__(self, age, skill, x, y, range_):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.skill = skill
        self.health = 10
        self.x = x
        self.y = y
        self.range = range_

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

def avgskill(lions):
    total_skill = sum(lion.skill for lion in lions)
    if len(lions) > 0:
        return total_skill / len(lions)
    else:
        return 0


def prey():
    for lion in LionDictionary:
        if lion.age > 8:
            if len(peopleDictionary) > 0 and len(peopleDictionary) / area > 1:
                potentialPreys = [p for p in peopleDictionary if distance(lion.x, lion.y, p.x, p.y) <= lion.range]
                if potentialPreys:
                    prey = random.choice(potentialPreys)
                    peopleDictionary.remove(prey)
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
                peopleDictionary.append(Person(0, person.x, person.y, person.range))
    for lion in LionDictionary:
        if lion.gender == 1 and fertilityx < lion.age < fertilityy:
                if random.randint(0, 3) == 1 and random.randint(0, 100) > LioninfantMortality:
                    ranskill = random.uniform(lion.skill - 0.5, lion.skill + 0.5)
                    LionDictionary.append(Lion(0, ranskill, lion.x, lion.y, lion.range))

def beginSim():
    for _ in range(startPopulation):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        range_ = random.uniform(1, 2)  # Range for each person
        peopleDictionary.append(Person(random.randint(18, 50), x, y, range_))
    for _ in range(startPopulation_Lion):
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)
        range_ = random.uniform(1, 3)  # Range for each lion
        LionDictionary.append(Lion(random.randint(18, 30), random.uniform(1, 2.5), x, y, range_))

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

        LionDictionary.append(Lion(10,4,x,y, random.uniform(1, 3)))  # Add lion with random range
        LionDictionary.append(Lion(10,4,x,y, random.uniform(1, 3)))  # Add lion with random range
        LionDictionary.append(Lion(10,4,x,y, random.uniform(1, 3)))  # Add lion with random range

beginSim()

# Create a figure and axis
fig, ax = plt.subplots()

# Set the limits of the plot
ax.set_xlim(0, 10)
ax.set_ylim(0, 10)


# Calculate Euclidean distance between two points (x1, y1) and (x2, y2)
def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

people_plot = ax.scatter([], [], c='blue', label='People')
lion_plot = ax.scatter([], [], c='red', label='Lions')

# Initialize the year counter
year = 2023

# Update function for the animation
def update(frame):
    global year

    # Calculate the current year based on the frame number
    year += 1

    # Run simulation for one year
    runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance, youthMortality, LioninfantMortality)

    # Update scatter plot data
    people_plot.set_offsets([(person.x, person.y) for person in peopleDictionary])
    lion_plot.set_offsets([(lion.x, lion.y) for lion in LionDictionary])

    # Calculate average skill
    averageskill = avgskill(LionDictionary)

    # Set title with average skill and year
    ax.set_title(f'Year: {year}\nAverage Skill: {averageskill:.2f} Lions:{len(LionDictionary)}\n Humans:{len(peopleDictionary)}')

# Create animation
animation = FuncAnimation(fig, update, frames=500, interval=10, repeat=False)

# Add legend
ax.legend()

# Show plot
plt.show()
