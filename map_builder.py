# ---- IMPORTS ---- #
import pygame
import map

map = map.map

pygame.init()

BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
GOLD = (255,215,0)
BROWN = (150,75,0)
TILE_SIZE = 64
TILES_PER_ROW = 30
map_y = 0
tile_type = 1

font = pygame.font.Font("assets/fonts/menu_font.ttf",30)

root = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

def info_text(coin_count,spawns_count,platforms_count):
    coin_text_string = f"Coins: {coin_count}"
    coin_text = font.render(coin_text_string,True,(100,100,100))
    pygame.draw.rect(root,BLACK,(0,0,len(coin_text_string)*15.5,34))
    root.blit(coin_text,(0,2))

    if spawns_count == 1:
        spawns_colour = BLUE
    else:
        spawns_colour = (100,100,100)
    spawns_text_string = f"Spawns: {spawns_count}/1"
    spawns_text = font.render(spawns_text_string,True,spawns_colour)
    pygame.draw.rect(root,BLACK,(0,34,len(spawns_text_string)*16,34))
    root.blit(spawns_text,(0,36))

    acorns_text_string = f"Acorns: {acorn_count}"
    acorns_text = font.render(acorns_text_string,True,(100,100,100))
    pygame.draw.rect(root,BLACK,(0,68,len(acorns_text_string)*16,34))
    root.blit(acorns_text,(0,70))

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()
    mouse_pos = pygame.mouse.get_pos()
    mouse_pressed = pygame.mouse.get_pressed()

    coin_count = 0
    platforms_count = 0
    spawns_count = 0
    acorn_count = 0

    root.fill(WHITE)

    if keys[pygame.K_e]:
        tile_type = 0
    if keys[pygame.K_q]:
        tile_type = 1
    if keys[pygame.K_c]:
        tile_type = 2
    if keys[pygame.K_x]:
        tile_type = 3
    if keys[pygame.K_t]:
        tile_type = 9
    

    if keys[pygame.K_LCTRL] and keys[pygame.K_r]:
        for row in range(len(map)):
            for col in range(len(map[row])):
                map[row][col] = 0 

    for row in range(len(map)):
        for col in range(len(map[row])):
            if map[row][col] == 1:
                pygame.draw.rect(root,BLACK,(col*TILE_SIZE,row*TILE_SIZE+map_y,TILE_SIZE, TILE_SIZE))
                platforms_count += 1
            if map[row][col] == 2:
                pygame.draw.rect(root,GOLD,(col*TILE_SIZE,row*TILE_SIZE+map_y,TILE_SIZE, TILE_SIZE))
                coin_count += 1
            if map[row][col] == 3:
                pygame.draw.rect(root,BROWN,(col*TILE_SIZE,row*TILE_SIZE+map_y,TILE_SIZE, TILE_SIZE))
                acorn_count += 1
            if map[row][col] == 9:
                pygame.draw.rect(root,BLUE,(col*TILE_SIZE,row*TILE_SIZE+map_y,TILE_SIZE, TILE_SIZE))
                spawns_count += 1
                spawn_placed = True
            pygame.draw.rect(root,BLACK,(col*TILE_SIZE,row*TILE_SIZE+map_y,TILE_SIZE, TILE_SIZE),1)

    if mouse_pressed[0]:
        mouse_y_location = mouse_pos[1] - map_y
        tile_x = int(mouse_pos[0]/TILE_SIZE)
        tile_y = int(mouse_y_location/TILE_SIZE)
        past_tile_type = map[tile_y][tile_x]
        if tile_type == 9:
            if spawn_placed == False:
                spawn_placed = True
                map[tile_y][tile_x] = tile_type
            else:
                map[tile_y][tile_x] = 0
        else:
            map[tile_y][tile_x] = tile_type
        
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        if map_y > -400 * TILE_SIZE + 1080:
            map_y -= 20
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        if map_y < 0:
            map_y += 20

    info_text(coin_count,spawns_count,platforms_count)

    spawn_placed = False

    pygame.display.flip()

pygame.quit()

file = open("map.py","w")
map_string = "map = ["
for row in range(400):
    map_row = str(map[row])
    map_row += ",\n"
    map_string += map_row

map_string += "]"
file.write(map_string)
file.close()
