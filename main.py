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
# Integers
TILE_SIZE = 64
SCREEN_WIDTH,SCREEN_HEIGHT = 1920,1080
# Booleans
running = True      # Whether the main game loop should run or not.
# Miscellaneous
vector = pygame.math.Vector2        # Standardising vectors so I needn't retype "pygame.math.Vector2" each time I declare a vector.
load = pygame.image.load
clock = pygame.time.Clock()     # Declaring the clock.
map = map.map       # The tilemap.
# Sprite groups
player_group = pygame.sprite.Group()
main_tile_group = pygame.sprite.Group()
dirt_tile_group = pygame.sprite.Group()
wall_tile_group = pygame.sprite.Group()


# ---- SETTING UP THE GAME WINDOW ---- #
root = pygame.display.set_mode((0,0), pygame.FULLSCREEN)        # Making the game window.
pygame.display.set_caption(GAME_NAME)       # Setting the window caption to the game name.


# ---- CLASSES ---- #
# ---- PLAYER CLASS
class PLAYER(pygame.sprite.Sprite):
    # Initialising the player.
    def __init__(self,x,y,collision_tiles):
        super().__init__()

        # Image variables
        self.image = load("assets/images/player/player_facing_right.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        # Collision tiles.
        self.collision_tiles = collision_tiles
        self.on_platform = False

        # Kinematic variables
        self.multiplier = 0
        self.has_jump = True
        self.position = vector(x,y)     # Position vector.
        self.velocity = vector(0,0)     # Velocity vector.
        self.acceleration = vector(0,0)     # Acceleration vector.

        # Physics/kinematic constants
        self.HORIZONTAL_ACCELERATION = 2        # The acceleration of the player when moving left and right.
        self.FRICTION_COEFFICIENT = 0.1     # The coefficient of friction of the player.
        self.GRAVITY = 0.2      # How much gravity effects the player.

    # Updating the player.
    def update(self):
        if self.velocity.y <= 7:
            self.acceleration = vector(0,self.GRAVITY)     # Reseting the acceleration to fix bouncing bug.
        else:
            self.acceleration = vector(0,0)
        self.multiplier = 0     # Multiplier for velocity. This is so that if you press both A and D, you do not move.

        if keys[pygame.K_d]:
            self.multiplier += 1        # Positive multiplier to increase x value.
            self.image = load("assets/images/player/player_facing_right.png")       # Loading the facing right image.
        if keys[pygame.K_a]:
            self.multiplier -= 1        # Negative multiplier to decrease y value.
            self.image = load("assets/images/player/player_facing_left.png")        # Loading the facing left image.
        if keys[pygame.K_SPACE]:
            if self.velocity.y > -1.5:      # Giving a limit to how fast the glide can be.
                self.acceleration.y = -1 * self.GRAVITY     # Decelerating at the same rate as gravity.
        if keys[pygame.K_w]:
            if self.has_jump:
                self.velocity.y = -10


        # Kinematic movement equations.
        self.acceleration.x = self.HORIZONTAL_ACCELERATION * self.multiplier

        self.acceleration.x -= self.velocity.x * self.FRICTION_COEFFICIENT
        self.velocity += self.acceleration
        self.position += self.velocity + self.acceleration / 2

        # Checking if the squirrel is off the screen.
        if self.position.x > 2000:
            self.position.x = -100      # Putting the player off the screen on the far left.
            self.position.y -= 50       # To allow for smoother movement.
        if self.position.x < -100:
            self.position.x = 2000     # Putting the player off the screen on the far right.
            self.position.y -= 50       # To allow for smoother transportation.

        self.rect.bottomright = self.position        # Setting the new position

        # Checking if player collides with map.
        touched_tiles = pygame.sprite.spritecollide(self,self.collision_tiles,False)        # Making a list of all tiles that are touching the player.

        if touched_tiles:
            if self.rect.bottom - 15 < touched_tiles[0].rect.top:       # Checking if the player came from above the tile.
                self.has_jump = True
                self.position.y = touched_tiles[0].rect.top 
                self.velocity.y = 0
        else:
            self.has_jump = False


# ---- TILE CLASS
class TILE(pygame.sprite.Sprite):
    # Initialising the map.
    def __init__(self,x,y,tile_int,main_group,sub_group,player_group):
        super().__init__()

        if tile_int == 1:
            self.image = load("assets/images/tiles/tile_dirt_texture.png")
            sub_group.add(self)
        if tile_int == 2:
            self.image = load("assets/images/tiles/tile_dirt_texture.png")
            sub_group.add(self)
        
        main_group.add(self)

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.player_group = player_group

        self.position = vector(x,y)

        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.GRAVITY = 0.05

    
    def update(self):
        keys = pygame.key.get_pressed()

        if self.velocity.y <= -5:
            self.acceleration.y = 0
        else:
            self.acceleration = vector(0,self.GRAVITY)

        self.velocity -= self.acceleration
        self.position += self.velocity + self.acceleration / 2

        self.rect.topleft = self.position
       

# ---- MAKING THE MAP ---- #
for row in range(len(map)):
    for col in range(len(map[row])):
        if map[row][col] == 1:
            tile = TILE(col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,dirt_tile_group,player_group)
        if map[row][col] == 2:
            tile = TILE(col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,wall_tile_group,player_group)
        if map[row][col] == 9:
            player = PLAYER(col*TILE_SIZE,row*TILE_SIZE,dirt_tile_group)
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
    root.fill(GREY)        # Resetting the window to allow a new frame to be drawn.

    main_tile_group.update()        # Updating the tilemap
    main_tile_group.draw(root)      # Drawing the tilemap.

    player_group.update()     # Updating the player class.
    player_group.draw(root)     # Drawing the player.

    pygame.display.flip()       # Flipping the display.

pygame.quit()       # Closing the window.