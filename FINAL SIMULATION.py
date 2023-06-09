import random
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np
from matplotlib.widgets import Button
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt2
import pygame

matplotlib.use('TkAgg')
pygame.init()

# Function to play background music
def play_bgm():
    pygame.mixer.music.load('The Blue Planet.mp3')
    pygame.mixer.music.play(-1)
# Initialize pygame mixer and play the background music
pygame.mixer.init()
play_bgm()
music_paused = False
startPopulation_Lion = 20
startPopulation = 300
infant_mortality = 10
Lioninfant_mortality = 10
youth_mortality = 5
agriculture = 5
disaster_chance = 10
min_age_fertility = 18
max_age_fertility = 40
food = 1
peopleDictionary = []
LionDictionary = []
area = 100
averageskill = 0
humanaverage_age = 0
lionaverage_age = 0
humanaverage_speed = 0
lionaverage_speed = 0
humanaverage_range = 0
lionaverage_range = 0
mutation = 1  # Initial value for mutation
rain = 1  # Initial value for rain factor


class Person:
    def __init__(self, age, x, y, range_, speed):
        self.gender = random.randint(0, 1)
        self.age = age
        self.x = x
        self.y = y
        if range_> 0:
            self.range = range_
        else:
            self.range =0
        if range_> 0:
            self.speed = speed
        else:
            self.speed = 0
    def move(self):
        # Check if there are any lions within the range
        nearby_lions = [lion for lion in LionDictionary if
                        distancesquare(self.x, self.y, lion.x, lion.y) <= self.range ** 2]
        nearby_people = [person for person in peopleDictionary if
                         self != person and distancesquare(self.x, self.y, person.x, person.y) <= self.range ** 2]
        # If there are nearby lions, try to move away from them
        if nearby_lions:
            lion_x, lion_y = nearby_lions[0].x, nearby_lions[0].y

            # Calculate the direction away from the lion
            dx = self.x - lion_x
            dy = self.y - lion_y

            # Normalize the direction vector
            magnitude = (dx ** 2 + dy ** 2) ** 0.5
            if magnitude > 0:
                dx /= magnitude
                dy /= magnitude

            # Move away from the lion by adding the direction vector
            self.x += dx * self.speed
            self.y += dy * self.speed
        elif len(nearby_people) > 20:
            self.x += random.uniform(-1, 1)
            self.y += random.uniform(-1, 1)
        else:
            self.x += random.uniform(-0.1, 0.1)  # People will run with speed only  when lion is near
            self.y += random.uniform(-0.1, 0.1)

        # Ensure the person stays within the boundaries
        self.x = max(0, min(20, self.x))
        self.y = max(0, min(20, self.y))


class Lion:
    def __init__(self, age, skill, x, y, range_, speed):
        self.gender = random.randint(0, 1)
        self.age = age
        self.skill = skill
        self.health = 5
        self.x = x
        self.y = y
        if range_> 0:
            self.range = range_
        else:
            self.range =0
        if range_> 0:
            self.speed = speed
        else:
            self.speed = 0

    def move(self):
        # Check if there are any people within the range
        nearby_people = [person for person in peopleDictionary if
                         distancesquare(self.x, self.y, person.x, person.y) <= self.range ** 2]

        nearby_lions = [lion for lion in LionDictionary if
                        lion != self and distancesquare(self.x, self.y, lion.x, lion.y) <= self.range ** 2]

        # If there are nearby people, try to move towards them
        if nearby_people:
            person_x, person_y = nearby_people[0].x, nearby_people[0].y
            # Calculate the direction towards the person
            dx = person_x - self.x
            dy = person_y - self.y
            # Normalize the direction vector
            magnitude = (dx ** 2 + dy ** 2) ** 0.5
            if magnitude > 0:
                dx /= magnitude
                dy /= magnitude

            # Move towards the person by adding the direction vector
            self.x += dx * self.speed
            self.y += dy * self.speed
        elif len(nearby_lions) > 5:
            self.x += random.uniform(-1, 1)
            self.y += random.uniform(-1, 1)
            # Ensure the lion stays within the boundaries
            self.x = max(0, min(20, self.x))
            self.y = max(0, min(20, self.y))
        else:
            self.x += random.uniform(-0.5, 0.5)
            self.y += random.uniform(-0.5, 0.5)
        # Ensure the lion stays within the boundaries
        self.x = max(0, min(20, self.x))
        self.y = max(0, min(20, self.y))
def pause_music(event):
    global music_paused
    if not music_paused:
        pygame.mixer.music.pause()
        music_paused = True

def play_music(event):
    global music_paused
    if music_paused:
        pygame.mixer.music.unpause()
        music_paused = False


def distancesquare(x1, y1, x2, y2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2


def harvest(food, agriculture):
    global rain
    ablepeople = 0
    # to reduce the for loop we are giving these functions inside this folder
    for person in peopleDictionary:
        if person.age > 8:
            ablepeople += 1
        if person.age > 80:
            peopleDictionary.remove(person)
        else:
            person.age += 1
            person.move()
    food += ablepeople * agriculture * rain

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
        if lion.age > 3:
            if len(peopleDictionary) > 0 and lion.health < 5:
                potentialpreys = [p for p in peopleDictionary if
                                  distancesquare(lion.x, lion.y, p.x, p.y) <= lion.range ** 2]
                if potentialpreys:
                    prey = random.choice(potentialpreys)
                    peopleDictionary.remove(prey)
                    lion.health += lion.skill
                else:
                    lion.health -= 1
            else:
                lion.health -= 1
        if lion.health < 1:
            LionDictionary.remove(lion)
        if lion.age > 20 and lion.health >= 1:
            LionDictionary.remove(lion)  # to reduce the for loop we are giving these functions inside this folder
        else:
            lion.age += 1
            lion.move()


def reproduce(min_age_fertility, max_age_fertility, infant_mortality, Lioninfant_mortality):
    global humanaverage_age
    global lionaverage_age
    global humanaverage_speed
    global lionaverage_speed
    global humanaverage_range
    global lionaverage_range
    global mutation
    humanaverage_age = 0
    lionaverage_age = 0
    humanaverage_speed = 0
    lionaverage_speed = 0
    humanaverage_range = 0
    lionaverage_range = 0
    for person in peopleDictionary:
        humanaverage_age += person.age / len(peopleDictionary)
        humanaverage_speed += person.speed / len(peopleDictionary)
        humanaverage_range += person.range / len(peopleDictionary)
        if person.gender == 1 and min_age_fertility < person.age < max_age_fertility:
            if random.randint(0, 5) == 1 and random.randint(0, 100) > infant_mortality:
                peopleDictionary.append(Person(0, person.x, person.y, person.range + random.uniform(-1, 1) * mutation,
                                               person.speed +
                                               random.uniform(-0.5, 0.5) * mutation))  # adding mutation to range traits
    for lion in LionDictionary:
        lionaverage_age += lion.age / len(LionDictionary)
        lionaverage_speed += lion.speed / len(LionDictionary)
        lionaverage_range += lion.range / len(LionDictionary)
        if lion.gender == 1 and 3 < lion.age < 15:
            if random.randint(0, 2) == 1 and random.randint(0, 100) > Lioninfant_mortality:
                ranskill = lion.skill + random.uniform(-0.5, 0.5) * mutation
                LionDictionary.append(Lion(0, ranskill, lion.x, lion.y, lion.range + random.uniform(-1, 1) * mutation,
                                           lion.speed +
                                           random.uniform(-0.5, 0.5) * mutation))  # adding mutation to range traits


def begin_simulation():
    for i in range(startPopulation):
        x = random.uniform(0, 20)
        y = random.uniform(0, 20)
        range_ = random.uniform(1, 3)  # Range for each person
        speed = random.uniform(0.5, 1)
        peopleDictionary.append(Person(random.randint(18, 50), x, y, range_, speed))
    for j in range(startPopulation_Lion):
        x = random.uniform(0, 20)
        y = random.uniform(0, 20)
        range_ = random.uniform(1, 3)  # Range for each lion
        speed = random.uniform(0.5, 2)
        LionDictionary.append(Lion(random.randint(3, 15), random.uniform(1, 2.5), x, y, range_, speed))


def runyear(food, agriculture, min_age_fertility, max_age_fertility, infant_mortality, disaster_chance, youth_mortality,
            Lioninfant_mortality):
    harvest(food, agriculture)
    prey()
    reproduce(min_age_fertility, max_age_fertility, infant_mortality, Lioninfant_mortality)

    if random.randint(0, 100) < disaster_chance:
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]

    infant_mortality *= 0.985

    if random.randint(0, 100) < youth_mortality:
        del peopleDictionary[0:int(random.uniform(0.05, 0.2) * len(peopleDictionary))]

    youth_mortality *= 0.9
    if random.randint(0, 300) == 50:
        x = random.uniform(0, 10)
        y = random.uniform(0, 10)

        LionDictionary.append(Lion(5, 2, x, y, random.uniform(1, 3), 1))  # Add lion with random range
        LionDictionary.append(Lion(5, 2, x, y, random.uniform(1, 3), 1.5))  # Add lion with random range
        LionDictionary.append(Lion(5, 2, x, y, random.uniform(1, 3), 1))  # Add lion with random range


def update_mutation(val):
    global mutation
    mutation = val


def update_rain(val):
    global rain
    rain = val


# Slider callback function
def update_zoom(val):
    ax.dist = val
    fig.canvas.draw_idle()


begin_simulation()
fig, ax2 = plt2.subplots(3, sharex=True, sharey=False)
# Create a 3D figure and axis
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
# Set viewing angle and zoom level
ax.view_init(elev=30, azim=45)  # Set the elevation and azimuth angles
# Set initial zoom level
initial_zoom = 8
ax.dist = initial_zoom
# Set the limits of the plot in the XY plane
ax.set_xlim(-1, 21)
ax.set_ylim(-1, 21)

ax.xaxis.set_pane_color((0.53, 0.81, 0.92, 1.0))  # Sky blue
ax.yaxis.set_pane_color((0.53, 0.81, 0.92, 1.0))
ax.zaxis.set_pane_color((0.1, 1, 0.1, 1.0))
population_sizes = []
population_sizesLions = []
lionavg_skill = []
human_average_age = []
lion_average_age = []
human_average_speed = []
lion_average_speed = []
human_average_range = []
lion_average_range = []

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

add_lion_button_ax = plt.axes([0.80, 0.885, 0.025, 0.025])
add_lion_button = Button(add_lion_button_ax, '+', color='0.9', hovercolor='red', )

add_people_button_ax = plt.axes([0.80, 0.915, 0.025, 0.025])
add_people_button = Button(add_people_button_ax, '+', color='0.9', hovercolor='blue', )

play_button_ax = plt.axes([0.7, 0.05, 0.1, 0.05])
play_button = Button(play_button_ax, 'Play', hovercolor='0.9')
# Create a slider widget
ax_slider = plt.axes([0.1, 0.05, 0.15, 0.03])
zoom_slider = Slider(ax_slider, 'Zoom', valmin=5, valmax=10, valinit=initial_zoom)
zoom_slider.on_changed(update_zoom)
# Create a slider widget for mutation
ax_mutation = plt.axes([0.1, 0.1, 0.15, 0.03])
mutation_slider = Slider(ax_mutation, 'Mutation', valmin=0, valmax=2, valinit=mutation)
mutation_slider.on_changed(update_mutation)
# Create a slider widget for rain
ax_rain = plt.axes([0.1, 0.15, 0.15, 0.03])
rain_slider = Slider(ax_rain, 'Rain', valmin=0, valmax=2.5, valinit=rain)
rain_slider.on_changed(update_rain)

# Flag to control animation state
animation_paused = False


# Update function for the animation
def update(frame):
    try:
        # if len(peopleDictionary)<=1:
        #     return
        if len(LionDictionary) <= 2:
            LionDictionary.append(Lion(5, 2, random.uniform(0, 20), random.uniform(0, 20), random.uniform(1, 3), 1))
        global year
        global humanaverage_age
        global lionaverage_age
        global humanaverage_speed
        global lionaverage_speed
        global humanaverage_range
        global lionaverage_range
        if animation_paused:
            return
        # Calculate the current year based on the frame number
        year += 1

        # Run simulation for one year
        runyear(food, agriculture, min_age_fertility, max_age_fertility,
                infant_mortality, disaster_chance, youth_mortality, Lioninfant_mortality)
        # Update scatter plot data with Z-axis coordinates
        people_offsets = np.array([[person.x, person.y, 0] for person in peopleDictionary])
        lion_offsets = np.array([[lion.x, lion.y, 0] for lion in LionDictionary])
        people_plot._offsets3d = people_offsets.T
        lion_plot._offsets3d = lion_offsets.T
        # Calculate average skill
        averageskill = avgskill(LionDictionary)

        # Set title with average skill and year
        ax.set_title(
            f'Year: {year}\nAverage Skill: {averageskill:.2f} Lions:{len(LionDictionary)}\n'
            f' Humans:{len(peopleDictionary)}')
        # Update population data
        population_sizes.append(len(peopleDictionary))
        population_sizesLions.append(len(LionDictionary))
        lionavg_skill.append(averageskill)
        human_average_age.append(humanaverage_age)
        lion_average_age.append(lionaverage_age)
        human_average_speed.append(humanaverage_speed)
        human_average_range.append(humanaverage_range)
        lion_average_speed.append(lionaverage_speed)
        lion_average_range.append(lionaverage_range)

        ax2[0].clear()
        ax2[0].plot(range(year), population_sizes, color='blue', label='Humans Population')
        ax2[0].plot(range(year), population_sizesLions, color='red', label='Lions Population')
        ax2[0].legend()
        ax2[1].clear()
        ax2[1].plot(range(year), human_average_speed, color='blue', label='Humans avg speed')
        ax2[1].plot(range(year), human_average_range, color='purple', label='Humans avg range')
        ax2[1].plot(range(year), lion_average_speed, color='orange', label='lions avg speed')
        ax2[1].plot(range(year), lion_average_range, color='yellow', label='lions avg range')
        # ax2[1].plot(range(year), lionavg_skill , color='red', label='Lions average Skill')
        ax2[1].legend()
        ax2[2].clear()
        ax2[2].plot(range(year), human_average_age, color='blue', label='Humans average age')
        ax2[2].plot(range(year), lion_average_age, color='red', label='Lions average age')
        ax2[2].legend()
        ax2[0].set_ylabel('Population')
        ax2[0].set_title('Population Comparison')
        ax2[1].set_ylabel('Speed and Range')
        ax2[1].set_title('Average Speed and Range Comparison')
        ax2[2].set_xlabel('Year')
        ax2[2].set_ylabel('Average Age')
        ax2[2].set_title('Average Age Comparison')
        ax2[0].legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize='smaller')
        ax2[1].legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize='smaller')
        ax2[2].legend(loc='upper left', bbox_to_anchor=(0, 1), fontsize='smaller')

        plt.setp(ax2[0].get_legend().get_texts(), fontsize='small')  # Set legend text font size
        plt.setp(ax2[1].get_legend().get_texts(), fontsize='small')  # Set legend text font size
        plt.setp(ax2[2].get_legend().get_texts(), fontsize='small')  # Set legend text font size

        plt2.show()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        year += 1


# Button click event handlers
def pause_animation(event):
    global animation_paused
    animation_paused = True
    animation.event_source.stop()


def add_lion(event):
    LionDictionary.append(Lion(5, 2, random.uniform(0, 20), random.uniform(0, 20), random.uniform(1, 2), 1.5))


def add_people(event):
    peopleDictionary.append(Person(15, random.uniform(0, 20), random.uniform(0, 20), random.uniform(1, 2), 1.5))


def play_animation(event):
    global animation_paused
    animation_paused = False
    animation.event_source.start()


# Set button click event handlers
pause_button.on_clicked(pause_animation)
play_button.on_clicked(play_animation)
add_lion_button.on_clicked(add_lion)
add_people_button.on_clicked(add_people)
pause_button.on_clicked(pause_music)
play_button.on_clicked(play_music)
# Create animation
animation = FuncAnimation(fig, update, frames=300, interval=100, repeat=False, blit=False)
# Add legend
ax.legend()
ax.legend(loc='upper left', bbox_to_anchor=(0.9, 1.1), fontsize='small')
# Show plot
plt.show()
