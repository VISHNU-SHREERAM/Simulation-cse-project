import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
matplotlib.use('TkAgg')
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.widgets import Button

startPopulation_Lion = 5
startPopulation = 200
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
    def __init__(self, age, x, y, range_,speed):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.x = x
        self.y = y
        self.range = range_
        self.speed = speed

    def move(self):
        # Check if there are any lions within the range
        nearby_lions = [lion for lion in LionDictionary if distance(self.x, self.y, lion.x, lion.y) <= self.range]

        # If there are nearby lions, try to move away from them
        if nearby_lions:
            lion_x, lion_y = nearby_lions[0].x, nearby_lions[0].y

            # Calculate the direction away from the lion
            dx = self.x - lion_x
            dy = self.y - lion_y

            # Normalize the direction vector
            magnitude = np.sqrt(dx**2 + dy**2)
            if magnitude > 0:
                dx /= magnitude
                dy /= magnitude

            # Move away from the lion by adding the direction vector
            self.x += dx * self.speed
            self.y += dy * self.speed
        else:
            self.x += random.uniform(-0.1, 0.1)  #People will run with speed only  when lion is near
            self.y += random.uniform(-0.1, 0.1)

        # Ensure the person stays within the boundaries
        self.x = max(0, min(20, self.x))
        self.y = max(0, min(20, self.y))

class Lion:
    def __init__(self, age, skill, x, y, range_,speed):
        self.gender = random.randint(0, 1)
        self.age = age
        self.pregnant = 0
        self.skill = skill
        self.health = 5
        self.x = x
        self.y = y
        self.range = range_
        self.speed = speed

    def move(self):
        # Check if there are any people within the range
        nearby_people = [person for person in peopleDictionary if distance(self.x, self.y, person.x, person.y) <= self.range]


        nearby_lions = [lion for lion in LionDictionary if lion != self and distance(self.x, self.y, lion.x, lion.y) <= self.range]

        # If there are nearby people, try to move towards them
        if nearby_people:
            person_x, person_y = nearby_people[0].x, nearby_people[0].y



            # Calculate the direction towards the person
            dx = person_x - self.x
            dy = person_y - self.y
            # Normalize the direction vector
            magnitude = np.sqrt(dx**2 + dy**2)
            if magnitude > 0:
                dx /= magnitude
                dy /= magnitude

            # Move towards the person by adding the direction vector
            self.x += dx * self.speed
            self.y += dy * self.speed
        elif len(nearby_lions)>5:
            self.x += random.uniform(-1, 1)
            self.y += random.uniform(-1, 1)
        # Ensure the lion stays within the boundaries
            self.x = max(0, min(20, self.x))
            self.y = max(0, min(20, self.y))
        else:
            self.x += random.uniform(-0.1, 0.1)
            self.y += random.uniform(-0.1, 0.1)
        # Ensure the lion stays within the boundaries
            self.x = max(0, min(20, self.x))
            self.y = max(0, min(20, self.y))

def distance(x1, y1, x2, y2):
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

def harvest(food, agriculture):
    ablePeople = 0
    for person in peopleDictionary:   ##to reduce the for loop we are giving these functions inside this folder
        if person.age > 8:
            ablePeople += 1
        if person.age >80:
            peopleDictionary.remove(person)
        else:
            person.age += 1
            person.move()
        

            
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
            if len(peopleDictionary) > 0 and len(peopleDictionary) / area > 1 and lion.health < 5:
                potentialPreys = [p for p in peopleDictionary if distance(lion.x, lion.y, p.x, p.y) <= lion.range]
                if potentialPreys:
                    prey = random.choice(potentialPreys)
                    peopleDictionary.remove(prey)
                    lion.health += lion.skill

            else:
                lion.health -= 1
                if lion.health < 1:
                    LionDictionary.remove(lion)
        if lion.age > 50 and lion.health>=1:
            LionDictionary.remove(lion)        #to reduce the for loop we are giving these functions inside this folder
        else:
            lion.age += 1
            lion.move()


def reproduce(fertilityx, fertilityy, infantMortality, LioninfantMortality):
    for person in peopleDictionary:
        if person.gender == 1 and fertilityx < person.age < fertilityy:
            if random.randint(0, 5) == 1 and random.randint(0, 100) > infantMortality:
                peopleDictionary.append(Person(0, person.x, person.y, person.range+random.uniform(-1,1),person.speed+random.uniform(-0.5,0.5)))#adding mutation to range traits
    for lion in LionDictionary:
        if lion.gender == 1 and fertilityx < lion.age < fertilityy:
                if random.randint(0, 3) == 1 and random.randint(0, 100) > LioninfantMortality:
                    ranskill = random.uniform(lion.skill - 0.5, lion.skill + 0.5)
                    LionDictionary.append(Lion(0, ranskill, lion.x, lion.y, lion.range+random.uniform(-1,1),lion.speed+random.uniform(-0.5,0.5)))#adding mutation to range traits
def beginSim():
    for i in range(startPopulation):
        x = random.uniform(0, 20)
        y = random.uniform(0, 20)
        range_ = random.uniform(1, 2)  # Range for each person
        speed = random.uniform(0.5,1)
        peopleDictionary.append(Person(random.randint(18, 50), x, y, range_,speed))
    for j in range(startPopulation_Lion):
        x = random.uniform(0, 20)
        y = random.uniform(0, 20)
        range_ = random.uniform(1, 3)  # Range for each lion
        speed = random.uniform(0.5,1)
        LionDictionary.append(Lion(random.randint(18, 30), random.uniform(1, 2.5), x, y, range_,speed))

def runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance, youthMortality, LioninfantMortality):
    harvest(food, agriculture)
    prey()
    
    """for person in peopleDictionary:
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
            lion.move()"""

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

        LionDictionary.append(Lion(10,4,x,y, random.uniform(1, 3),1))  # Add lion with random range
        LionDictionary.append(Lion(10,4,x,y, random.uniform(1, 3),1.5))  # Add lion with random range
        LionDictionary.append(Lion(10,4,x,y, random.uniform(1, 3),1))  # Add lion with random range

beginSim()
# Create a 3D figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Set the limits of the plot in the XY plane
ax.set_xlim(-1, 21)
ax.set_ylim(-1, 21)

# Update the scatter plot data with Z-axis coordinates
people_offsets = np.array([(person.x, person.y, 0) for person in peopleDictionary])
lion_offsets = np.array([(lion.x, lion.y, 0) for lion in LionDictionary])
people_plot = ax.scatter([], [], [], marker='o', c='blue', label='People', s=15)
lion_plot = ax.scatter([], [], [], c='red', label='Lions', s=15)
# Initialize the year counter
year = 0
# Create pause and play buttons
pause_button_ax = plt.axes([0.81, 0.05, 0.1, 0.05])
pause_button = Button(pause_button_ax, 'Pause', hovercolor='0.9')

play_button_ax = plt.axes([0.7, 0.05, 0.1, 0.05])
play_button = Button(play_button_ax, 'Play', hovercolor='0.9')

# Flag to control animation state
animation_paused = False
# Update function for the animation
def update(frame):
    global year
    if animation_paused:
        return
    # Calculate the current year based on the frame number
    year += 1

    # Run simulation for one year
    runYear(food, agriculture, fertilityx, fertilityy, infantMortality, disasterChance, youthMortality, LioninfantMortality)
    # Update scatter plot data with Z-axis coordinates
    people_offsets = np.array([[person.x, person.y, 0] for person in peopleDictionary])
    lion_offsets = np.array([[lion.x, lion.y, 0] for lion in LionDictionary])
    people_plot._offsets3d = people_offsets.T
    lion_plot._offsets3d = lion_offsets.T
    # Calculate average skill
    averageskill = avgskill(LionDictionary)

    # Set title with average skill and year
    ax.set_title(f'Year: {year}\nAverage Skill: {averageskill:.2f} Lions:{len(LionDictionary)}\n Humans:{len(peopleDictionary)}')
    # Button click event handlers
def pause_animation(event):
    global animation_paused
    animation_paused = True
    animation.event_source.stop()
def play_animation(event):
    global animation_paused
    animation_paused = False
    animation.event_source.start()
# Set button click event handlers
pause_button.on_clicked(pause_animation)
play_button.on_clicked(play_animation)
# Create animation
animation = FuncAnimation(fig, update, frames=200, interval=100, repeat=False, blit=False)
# Add legend
ax.legend()

# Show plot
plt.show()