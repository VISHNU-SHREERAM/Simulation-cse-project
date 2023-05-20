import random
import matplotlib.pyplot as plt
startPopulation_Lion = 15
startPopulation = 300
infantMortality = 15
LioninfantMortality=0
youthMortality = 10
agriculture = 5
disasterChance = 10
fertilityx = 18
fertilityy = 60
food = 1
peopleDictionary = []
LionDictionary = []
area = 10
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
    for lion in LionDictionary:
        if lion.age > 50:
            LionDictionary.remove(lion)
        else:
            lion.age += 1

    reproduce(fertilityx, fertilityy, infantMortality,LioninfantMortality)

    if random.randint(0, 100) < disasterChance:
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]
    #print(len(peopleDictionary))
    infantMortality *= 0.985
    if random.randint(0, 100) < youthMortality :
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]
    youthMortality *=0.9
    #print(len(peopleDictionary))
    if random.randint(0, 300)==50:
        LionDictionary.append(Lion(10,4))
        LionDictionary.append(Lion(10,4))
        LionDictionary.append(Lion(10,4))

beginSim()

population_sizes = []
population_sizesLions = []
year = 0
avgskills=[]

while len(peopleDictionary) < 10000 and len(peopleDictionary) > 1 and year < 3000:
    population_sizes.append(len(peopleDictionary))
    population_sizesLions.append(len(LionDictionary))
    avgskills.append(int(avgskill()))
    runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance,youthMortality,LioninfantMortality)
    year += 1
"""while len(peopleDictionary) < 1000 and len(peopleDictionary) > 1:
    print("Year:", year)
    print("People Population:", len(peopleDictionary))
    print("Lion Population:", len(LionDictionary))
    population_sizes.append(len(peopleDictionary))
    population_sizesLions.append(len(LionDictionary))
    runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance, youthMortality, LioninfantMortality)
    year += 1
    print()  # Add a blank line for clarity"""


# Plotting the population size over time
fig, ax = plt.subplots()
ax.plot(range(year),population_sizes, color='blue', label='humans Graph')
ax.plot(range(year),population_sizesLions, color='red', label='lion Graph')
ax.plot(range(year),avgskills, color='green', label='skill Graph')
plt.xlabel('Year')
plt.ylabel('Population Size')
plt.title('Population Simulation')
ax.legend()
plt.show()
