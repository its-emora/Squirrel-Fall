# ---- IMPORTS ---- #
import pygame
import random
import math
import map

pygame.init()       # Initialising PyGame.


# ---- VARIABLES ---- #
# Colours
BLACK = (0,0,0)     # Constants in FULL CAPS.
DARKGREY = (100,100,100)
GREY = (150,150,150)
LIGHTGREY = (200,200,200)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
# Strings
GAME_NAME = "Squirrel Fall"     # The game title.
# Booleans
running = True      # Whether the main game loop should run or not.
# Miscellaneous
vector = pygame.math.Vector2        # Standardising vectors so I needn't retype "pygame.math.Vector2" each time I declare a vector.
load = pygame.image.load
clock = pygame.time.Clock()     # Declaring the clock.
map = map.map       # The tilemap.
# Sprite groups
player_group = pygame.sprite.Group()




# ---- SETTING UP THE GAME WINDOW ---- #
root = pygame.display.set_mode((0,0), pygame.FULLSCREEN)        # Making the game window.
pygame.display.set_caption(GAME_NAME)       # Setting the window caption to the game name.


# ---- CLASSES ---- #
# ---- PLAYER CLASS
class PLAYER(pygame.sprite.Sprite):
    # Initialising the player.
    def __init__(self,x,y):
        super().__init__()

        # Image variables
        self.image = load("assets/images/player/player_facing_right.png")
        self.rect = self.image.get_rect()
        self.rect.center = (x,y)

        # Kinematic variables
        self.multiplier = 0
        self.position = vector(x,y)     # Position vector.
        self.velocity = vector(0,0)     # Velocity vector.
        self.acceleration = vector(0,0)     # Acceleration vector.

        # Physics/kinematic constants
        self.HORIZONTAL_ACCELERATION = 2        # The acceleration of the player when moving left and right.
        self.FRICTION_COEFFICIENT = 0.1     # The coefficient of friction of the player.
        self.GRAVITATIONAL_CONSTANT = 0.5       # The amount that gravity pulls down the player.

    # Updating the player.
    def update(self,dt):
        self.acceleration = vector(0,0)     # Reseting the acceleration to fix bouncing bug.
        self.multiplier = 0

        if keys[pygame.K_d]:
            self.multiplier += 0.5 
            self.image = load("assets/images/player/player_facing_right.png")
        if keys[pygame.K_a]:
            self.multiplier -= 0.5
            self.image = load("assets/images/player/player_facing_left.png")

        self.acceleration.x = self.HORIZONTAL_ACCELERATION * self.multiplier

        self.acceleration.x -= self.velocity.x * self.FRICTION_COEFFICIENT
        self.velocity += self.acceleration
        self.position += self.velocity + self.acceleration / 2 * dt

        if self.position.x > 2000:
            self.position.x = -100
        if self.position.x < -100:
            self.position.x = 2000

        self.rect.center = self.position


# ---- MAKING THE PLAYER ---- #
player = PLAYER(960,540)
player_group.add(player)


# ---- GAME LOOP ---- #
while running:
    # ---- QUIT QUEERY
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       # If the window is closed manually.
            running = False     # Setting the running value to false.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:        # If the user presses the escape key.
                running = False

    keys = pygame.key.get_pressed()     # Gettinmg the keys that the user has pressed.

    delta_time = clock.tick(60)/100     # Declaring delta time.
    root.fill(BLACK)        # Resetting the window to allow a new frame to be drawn.

    player_group.update(delta_time)
    player_group.draw(root)

    pygame.display.flip()       # Flipping the display.

pygame.quit()       # Closing the window.