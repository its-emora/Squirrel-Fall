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
TILE_SIZE = 64      # The size of each tile in pixels.
SCREEN_WIDTH,SCREEN_HEIGHT = 1920,1080      # The size of the screen in pixels.
SCREEN_CENTER = (SCREEN_WIDTH/2,SCREEN_HEIGHT/2)        # The coordinates of the center of the screen.
total_coins = 0     # Reseting the coin count.
total_acorns = 0        # Reseting the acorn count.
frame_count = 0
# Booleans
running = True      # Whether the main game loop should run or not.
start_menu = True       # Whether ther start_menu should display.
finish_menu = False
# Miscellaneous
vector = pygame.math.Vector2        # Standardising vectors so I needn't retype "pygame.math.Vector2" each time I declare a vector.
load = pygame.image.load        # Standardising loading so I needn't retype "pygame.image.load" every time I wish to load an image.
clock = pygame.time.Clock()     # Declaring the clock.
map = map.map       # The tilemap.
# Sprite groups
player_group = pygame.sprite.Group()        # Variable name speaks for itself.
main_tile_group = pygame.sprite.Group()
wood_tile_group = pygame.sprite.Group()
coin_tile_group = pygame.sprite.Group()
acorn_tile_group = pygame.sprite.Group()
finish_tile_group = pygame.sprite.Group()
# Images
menu_background = load("assets/images/backgrounds/full_logo.png")        # The menu bacground (scroll looking thing).
# Fonts
title_font = pygame.font.Font("assets/fonts/menu_font.ttf",60)      # The font for the game title.
title_font.set_underline(True)      # Underlining the game title.
menu_font = pygame.font.Font("assets/fonts/menu_font.ttf",30)       # The menu font (same as the title, just not underlined.)


# ---- SETTING UP THE GAME WINDOW ---- #
root = pygame.display.set_mode((0,0), pygame.FULLSCREEN)        # Making the game window.
pygame.display.set_caption(GAME_NAME)       # Setting the window caption to the game name.


# ---- SUBROUTINES ---- #
# ---- START MENU 
def startup_menu():
    global frame_count

    root.blit(menu_background,(0,0))        # Putting the menu background on the screen.


    frame_count += 1




def draw_stats(total_coins,player_coins,total_acorns,player_acorns):
    if player_coins == total_coins:     # Checking if the player has collected all the coins.
        coins_text_colour = GOLD        # Setting the coin stat colour to gold.
    else:
        coins_text_colour = WHITE       # Setting the coin stat colour to white.
    coins_text_string = f"Coins: {player_coins}/{total_coins}"      # Writing the coin stat string.
    coins_text = menu_font.render(coins_text_string,True,coins_text_colour)     # Rendering the coin stat text.
    pygame.draw.rect(root,BLACK,(0,0,len(coins_text_string)*16,34))      # Drawing the backdrop/highlight for the text to increase readability.
    root.blit(coins_text,(0,2))     # Putting the coin text on the screen.

    if player_acorns == total_acorns:       # Checking if the player hs all the acorns.
        acorns_text_colour  = BROWN     # Setting the acorn stat colour to brown.
    else:
        acorns_text_colour = WHITE      # Setting the acorn stat colour to white.
    acorns_text_string = f"Acorns: {player_acorns}/{total_acorns}"      # Writing the stat string.
    acorns_text = menu_font.render(acorns_text_string,True,acorns_text_colour)      # Rendering the acorn stat text.
    pygame.draw.rect(root,BLACK,(0,34,len(acorns_text_string)*16,34))       # Drawing the backdrop/highlight for the text to increase readability.
    root.blit(acorns_text,(0,36))       # Putting the stat on the screen.


# ---- CLASSES ---- #
# ---- PLAYER CLASS
class PLAYER(pygame.sprite.Sprite):
    # Initialising the player.
    def __init__(self,x,y,collision_tiles,coin_tiles):
        super().__init__()

        # Image variables
        self.image = load("assets/images/player/player_facing_right.png")       # Loading the player image.
        self.rect = self.image.get_rect()       # Getting the rect for the image.

        self.start_x = x
        self.start_y = y
        self.rect.bottomleft = (x,y)        # Setting the position for the player.

        # Stats.
        self.coins = 0      # Player's coin count.
        self.acorns = 0     # Player's acorn count.

        # Collision tiles.
        self.collision_tiles = collision_tiles      # The tiles that the player will collide with.
        self.on_platform = False        # Whether the player is on  platform or not. True --> Not falling
        self.dead = False

        # Kinematic variables
        self.multiplier = 0     # Multiplier for velocity.
        self.has_jump = True        # Seeing  if the user can use a jump.
        self.position = vector(x,y)     # Position vector.
        self.velocity = vector(0,0)     # Velocity vector.
        self.acceleration = vector(0,0)     # Acceleration vector.

        # Physics/kinematic constants
        self.HORIZONTAL_ACCELERATION = 2        # The acceleration of the player when moving left and right.
        self.FRICTION_COEFFICIENT = 0.1     # The coefficient of friction of the player.
        self.GRAVITY = 0.25      # How much gravity effects the player.

    # Updating the player.
    def update(self):
        self.dead = False

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
        self.acceleration.x = self.HORIZONTAL_ACCELERATION * self.multiplier        # Setting the player's x acceleration.

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

        self.rect.bottomright = self.position        # Setting the new position.

        # Checking if player collides with map.
        touched_tiles = pygame.sprite.spritecollide(self,self.collision_tiles,False)        # Making a list of all tiles that are touching the player.

        if touched_tiles:
            if self.rect.bottom - 20 < touched_tiles[0].rect.top:       # Checking if the player came from above the tile.
                self.has_jump = True
                self.position.y = touched_tiles[0].rect.top 
                self.velocity.y = 0
        else:
            self.has_jump = False       # Stopping the user from jumping on midair.

        # Checking if the player is no longer on the screen.
        if self.position.y < 0 or self.position.y > 1080 + 90:
            self.reset()
            self.dead = True

    def reset(self):
        self.acorns = 0 
        self.coins = 0

        self.acceleration = vector(0,0)
        self.velocity = vector(0,0)

        self.position = vector(self.start_x,self.start_y)
        self.rect.bottomleft = self.position

        



# ---- TILE CLASS
class TILE(pygame.sprite.Sprite):
    # Initialising the map.
    def __init__(self,map,x,y,tile_int,main_group,sub_group,player_group):
        super().__init__()

        if tile_int == 1:       # If the tile is a platform.
            self.image = load("assets/images/tiles/wood_texture.png")       # Loading the platform image.
            sub_group.add(self)
        if tile_int == 2:       # If the tile is a coin.
            self.image = load("assets/images/tiles/tile_coin.png")      # Loading the coin image.
            self.image = pygame.transform.scale(self.image,(32,32))
            sub_group.add(self)
        if tile_int == 3:       # If the tile is an acorn.
            self.image = load("assets/images/tiles/tile_acorn.png")     # Loading the acorn image.
            self.image = pygame.transform.scale(self.image,(100,100))
            sub_group.add(self)
        if tile_int == 8:
            self.image = load("assets/images/tiles/tile_finish_texture.png")
            sub_group.add(self)
        
        main_group.add(self)        # Adding all tiles to the main group.

        self.tile_int = tile_int

        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.start_x = x
        self.start_y = y

        self.player_group = player_group
    
        self.position = vector(x,y)
        if self.tile_int == 2:
            self.position += vector(16,8)
        if self.tile_int == 3:
            self.position -= vector(18,20)

        self.velocity = vector(0,0)
        self.acceleration = vector(0,0)
        self.GRAVITY = 0.1

    
    def update(self,main_tile_group):
        global finish_menu

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
                main_tile_group.remove(self)
                player.coins += 1
       
        if self.tile_int == 3:
            if pygame.sprite.spritecollide(self,self.player_group,False):
                main_tile_group.remove(self)
                player.acorns += 1

        if self.tile_int == 8:
            if pygame.sprite.spritecollide(self,self.player_group,False)
                finish_menu = True

        if player.dead:
            self.reset()

    def reset(self):

        self.acceleration = vector(0,0)
        self.velocity = vector(0,0)

        self.position = vector(self.start_x,self.start_y)
        self.rect.bottomleft = self.position

        if self.tile_int == 2:
            self.position += vector(16,8)
        if self.tile_int == 3:
            self.position -= vector(18,20)

        

# ---- MAKING THE MAP ---- #
for row in range(len(map)):
    for col in range(len(map[row])):
        if map[row][col] == 1:
            tile = TILE(map,col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,wood_tile_group,player_group)
        if map[row][col] == 2:
            tile = TILE(map,col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,coin_tile_group,player_group)
            total_coins += 1
        if map[row][col] == 3:
            tile = TILE(map,col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,acorn_tile_group,player_group)
            total_acorns += 1
        if map[row][col] == 8:
            tile = TILE(map,col*TILE_SIZE,row*TILE_SIZE,map[row][col],main_tile_group,finish_tile_group,player_group)
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
    elif finish_menu:
        pass
    else:
        delta_time = clock.tick(60)/100     # Declaring delta time.

        main_tile_group.update(main_tile_group)        # Updating the tilemap
        main_tile_group.draw(root)      # Drawing the tilemap.

        player_group.update()     # Updating the player class.
        player_group.draw(root)     # Drawing the player.

        draw_stats(total_coins,player.coins,total_acorns,player.acorns)

    pygame.display.flip()       # Flipping the display.

pygame.quit()       # Closing the window.
print(player.coins)
print(player.acorns)