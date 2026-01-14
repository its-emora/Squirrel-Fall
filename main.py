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
GOLD = (255,215,0)
BROWN = (150,75,0)
# Strings
GAME_NAME = "Squirrel Fall"     # The game title.
# Integers
TILE_SIZE = 64
SCREEN_WIDTH,SCREEN_HEIGHT = 1920,1080
SCREEN_CENTER = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)
total_coins = 0
total_acorns = 0
# Booleans
running = True      # Whether the main game loop should run or not.
start_menu = True
# Miscellaneous
vector = pygame.math.Vector2        # Standardising vectors so I needn't retype "pygame.math.Vector2" each time I declare a vector.
load = pygame.image.load
clock = pygame.time.Clock()     # Declaring the clock.
map = map.map       # The tilemap.
# Sprite groups
player_group = pygame.sprite.Group()
main_tile_group = pygame.sprite.Group()
wood_tile_group = pygame.sprite.Group()
coin_tile_group = pygame.sprite.Group()
acorn_tile_group = pygame.sprite.Group()
# Images
menu_background = load("assets/images/backgrounds/menu.png")
# Fonts
title_font = pygame.font.Font("assets/fonts/menu_font.ttf",60)
title_font.set_underline(True)
menu_font = pygame.font.Font("assets/fonts/menu_font.ttf",30)


# ---- SETTING UP THE GAME WINDOW ---- #
root = pygame.display.set_mode((0,0), pygame.FULLSCREEN)        # Making the game window.
pygame.display.set_caption(GAME_NAME)       # Setting the window caption to the game name.


# ---- SUBROUTINES ---- #
# ---- START MENU 
def startup_menu():
    root.blit(menu_background,(SCREEN_WIDTH/2 - 1120/2,SCREEN_HEIGHT/2 - 1120/2))

    title_text = title_font.render(GAME_NAME,True,BLACK)
    title_rect = title_text.get_rect()
    root.blit(title_text,(SCREEN_WIDTH/2-30*6,300))


def draw_stats(total_coins,player_coins,total_acorns,player_acorns):
    global WHITE,BLACK,GOLD,BROWN

    if player_coins == total_coins:
        coins_text_colour = GOLD
    else:
        coins_text_colour = WHITE
    coins_text_string = f"Coins: {player_coins}/{total_coins}"
    coins_text = menu_font.render(coins_text_string,True,coins_text_colour)
    pygame.draw.rect(root,BLACK,(0,0,len(coins_text_string)*16,34))
    root.blit(coins_text,(0,2))

    if player_acorns == total_acorns:
        acorns_text_colour  = BROWN
    else:
        acorns_text_colour = WHITE
    acorns_text_string = f"Acorns: {player_acorns}/{total_acorns}"
    acorns_text = menu_font.render(acorns_text_string,True,acorns_text_colour)
    pygame.draw.rect(root,BLACK,(0,34,len(acorns_text_string)*16,34))
    root.blit(acorns_text,(0,36))


# ---- CLASSES ---- #
# ---- PLAYER CLASS
class PLAYER(pygame.sprite.Sprite):
    # Initialising the player.
    def __init__(self,x,y,collision_tiles,coin_tiles):
        super().__init__()

        # Image variables
        self.image = load("assets/images/player/player_facing_right.png")
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x,y)

        # Stats.
        self.coins = 0
        self.acorns = 0

        # Collision tiles.
        self.coin_tiles = coin_tiles
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
        if self.velocity.y <= 10:
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
                self.velocity.y = -8


        # Kinematic movement equations.
        self.acceleration.x = self.HORIZONTAL_ACCELERATION * self.multiplier

        self.acceleration.x -= self.velocity.x * self.FRICTION_COEFFICIENT
        self.velocity += self.acceleration
        self.position += self.velocity + self.acceleration / 2

        # Checking if the squirrel is off the screen.
        if self.position.x > 1920+145:
            self.position.x = -100      # Putting the player off the screen on the far left.
            self.position.y -= 50       # To allow for smoother movement.
        if self.position.x < -100:
            self.position.x = 2000     # Putting the player off the screen on the far right.
            self.position.y -= 50       # To allow for smoother transportation.

        self.rect.bottomright = self.position        # Setting the new position

        # Checking if player collides with map.
        touched_tiles = pygame.sprite.spritecollide(self,self.collision_tiles,False)        # Making a list of all tiles that are touching the player.

        if touched_tiles:
            if self.rect.bottom - 20 < touched_tiles[0].rect.top:       # Checking if the player came from above the tile.
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
            self.image = load("assets/images/tiles/wood_texture.png")
            sub_group.add(self)
        if tile_int == 2:
            self.image = load("assets/images/tiles/tile_coin.png")
            self.image = pygame.transform.scale(self.image,(32,32))
            sub_group.add(self)
        if tile_int == 3:
            self.image = load("assets/images/tiles/tile_acorn.png")
            self.image = pygame.transform.scale(self.image,(100,100))
            sub_group.add(self)
        
        main_group.add(self)

        self.tile_int = tile_int

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)

        self.player_group = player_group

        self.position = vector(x,y)
        if self.tile_int == 2:
            self.position += vector(16,8)
        if self.tile_int == 3:
            self.position -= vector(18,20)

        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.GRAVITY = 0.1

    
    def update(self,main_tile_group,coin_tile_group):
        keys = pygame.key.get_pressed()

        if self.velocity.y <= -5:
            self.acceleration.y = 0
        else:
            self.acceleration = vector(0,self.GRAVITY)

        if keys[pygame.K_SPACE]:
            if self.velocity.y > 7.5:      # Giving a limit to how fast the glide can be.
                self.acceleration.y = self.GRAVITY     # Decelerating at the same rate as gravity.

        self.velocity -= self.acceleration
        self.position += self.velocity + self.acceleration / 2
        
        self.rect.topleft = self.position

        if self.tile_int == 2:
            if pygame.sprite.spritecollide(self,self.player_group,False):
                coin_tile_group.remove(self)
                main_tile_group.remove(self)
                player.coins += 1
       
        if self.tile_int == 3:
            if pygame.sprite.spritecollide(self,self.player_group,False):
                acorn_tile_group.remove(self)
                main_tile_group.remove(self)
                player.acorns += 1


# ---- MAKING THE MAP ---- #
for row in range(len(map)):
    for col in range(len(map[row])):
        if map[row][col] == 1:
            tile = TILE(col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,wood_tile_group,player_group)
        if map[row][col] == 2:
            tile = TILE(col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,coin_tile_group,player_group)
            total_coins += 1
        if map[row][col] == 3:
            tile = TILE(col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,acorn_tile_group,player_group)
            total_acorns += 1
        if map[row][col] == 9:
            player = PLAYER(col*TILE_SIZE,row*TILE_SIZE,wood_tile_group,coin_tile_group)
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
    root.fill(GREY)        # Resetting the window to allow a new frame to be drawn.

    if start_menu:
        startup_menu()
        if keys[pygame.K_p]:
            start_menu = False
    else:
        delta_time = clock.tick(60)/100     # Declaring delta time.

        main_tile_group.update(main_tile_group,coin_tile_group)        # Updating the tilemap
        main_tile_group.draw(root)      # Drawing the tilemap.

        player_group.update()     # Updating the player class.
        player_group.draw(root)     # Drawing the player.

        draw_stats(total_coins,player.coins,total_acorns,player.acorns)

    pygame.display.flip()       # Flipping the display.

pygame.quit()       # Closing the window.
print(player.coins)
print(player.acorns)