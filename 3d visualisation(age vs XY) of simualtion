import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
startPopulation_Lion = 100
startPopulation = 3000
infantMortality = 10
LioninfantMortality=0
youthMortality = 0
agriculture = 5
disasterChance = 10
fertilityx = 18
fertilityy = 40
food = 1
peopleDictionary = []
LionDictionary = []
area = 100
averageskill=0

class Person:
    def __init__(self, age):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
class Lion:
    def __init__(self, age,skill):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.skill=skill
        self.health=10
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
    sum=0
    for lions in LionDictionary:
        sum+=lions.skill
    if len(LionDictionary)>0:
        return sum/len(LionDictionary)
    else:
        return 0
def prey():
    for Lion in LionDictionary:
        if Lion.age > 8:
            if len(peopleDictionary) > 0 and len(peopleDictionary)/area >1:
                start_index = int(random.randint(0, len(peopleDictionary)-1))
                end_index = start_index + 1
                del peopleDictionary[start_index:end_index]
                if Lion.health<10 and Lion.skill>1:
                    Lion.health=Lion.health+Lion.skill
            else:
                Lion.health=Lion.health-1
                if Lion.health<1:
                    LionDictionary.remove(Lion)
def reproduce(fertilityx, fertilityy, infantMortality,LioninfantMortality):
    for person in peopleDictionary:
        if person.gender == 1 and fertilityx < person.age < fertilityy:
            if random.randint(0, 5) == 1 and random.randint(0, 100) > infantMortality:
                peopleDictionary.append(Person(0))
    for lion in LionDictionary:
        if lion.gender == 1 and fertilityx < lion.age < fertilityy:
            if random.randint(0, 3) == 1 and random.randint(0, 100) > LioninfantMortality:
                #LionDictionary.append(Lion(0,random.uniform((Lion.skill-1),(Lion.skill+1))))
                ranskill=random.uniform((lion.skill-0.5), (lion.skill+0.5))
                LionDictionary.append(Lion(0,ranskill))


def beginSim():
    for _ in range(startPopulation):
        peopleDictionary.append(Person(random.randint(18, 50)))
    for i in range(startPopulation_Lion):
        LionDictionary.append(Lion(random.randint(18, 30),random.uniform(1,2.5)))

def runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance,youthMortality,LioninfantMortality):
    harvest(food, agriculture)
    prey()

    for person in peopleDictionary:
        if person.age > 80:
            peopleDictionary.remove(person)
        else:
            person.age += 1
    for Lion in LionDictionary:
        if Lion.age > 50:
            LionDictionary.remove(Lion)
        else:
            Lion.age += 1

    reproduce(fertilityx, fertilityy, infantMortality,LioninfantMortality)

    if random.randint(0, 100) < disasterChance:
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]
    #print(len(peopleDictionary))
    infantMortality *= 0.985
    if random.randint(0, 100) < youthMortality :
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]
    youthMortality *=0.9
    #print(len(peopleDictionary))
def visualizePopulation():
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Extract X, Y, Z coordinates for people
    people_x = [random.uniform(0, 10) for _ in range(len(peopleDictionary))]
    people_y = [random.uniform(0, 10) for _ in range(len(peopleDictionary))]
    people_z = [person.age for person in peopleDictionary]

    # Extract X, Y, Z coordinates for lions
    lions_x = [random.uniform(0, 10) for _ in range(len(LionDictionary))]
    lions_y = [random.uniform(0, 10) for _ in range(len(LionDictionary))]
    lions_z = [lion.age for lion in LionDictionary]

    # Plot people as blue dots
    ax.scatter(people_x, people_y, people_z, c='blue', label='People')

    # Plot lions as red dots
    ax.scatter(lions_x, lions_y, lions_z, c='red', label='Lions')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Age')

    ax.legend()
    plt.show()

beginSim()
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def update(frame):
    ax.cla() # Clear the current plot
    runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance, youthMortality, LioninfantMortality)

# Extract X, Y, Z coordinates for people
    people_x = [random.uniform(0, 10) for _ in range(len(peopleDictionary))]
    people_y = [random.uniform(0, 10) for _ in range(len(peopleDictionary))]
    people_z = [person.age for person in peopleDictionary]

# Extract X, Y, Z coordinates for lions
    lions_x = [random.uniform(0, 10) for _ in range(len(LionDictionary))]
    lions_y = [random.uniform(0, 10) for _ in range(len(LionDictionary))]
    lions_z = [lion.age for lion in LionDictionary]

# Plot people as blue dots
    ax.scatter(people_x, people_y, people_z, c='blue', label='People')

# Plot lions as red dots
    ax.scatter(lions_x, lions_y, lions_z, c='red', label='Lions')

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Age')

    ax.legend()
animation = FuncAnimation(fig, update, frames=range(500), interval=500)
plt.show()




"""population_sizes = []
population_sizesLions = []
year = 0
avgskills=[]

while len(peopleDictionary) < 10000 and len(peopleDictionary) > 1 and year < 500:
    population_sizes.append(len(peopleDictionary))
    population_sizesLions.append(len(LionDictionary))
    avgskills.append(int(avgskill()))
    runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance,youthMortality,LioninfantMortality)
    visualizePopulation()
    year += 1"""
