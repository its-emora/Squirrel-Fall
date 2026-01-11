# ---- IMPORTS ---- #
import pygame
import map

map = map.map

BLACK = (0,0,0)
BLUE = (0,0,255)
WHITE = (255,255,255)
TILE_SIZE = 64
TILES_PER_ROW = 30
map_y = 0
tile_type = 1

pygame.init()
root = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

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

    root.fill(WHITE)

    if keys[pygame.K_q]:
        tile_type = 1
    if keys[pygame.K_e]:
        tile_type = 0
    if keys[pygame.K_t]:
        tile_type = 9

    if keys[pygame.K_LCTRL] and keys[pygame.K_r]:
        for row in range(len(map)):
            for col in range(len(map[row])):
                map[row][col] = 0 

    for row in range(len(map)):
        for col in range(len(map[row])):
            pygame.draw.rect(root,BLACK,(col*TILE_SIZE,row*TILE_SIZE+map_y,TILE_SIZE, TILE_SIZE),1)
            if map[row][col] == 1:
                pygame.draw.rect(root,BLACK,(col*TILE_SIZE,row*TILE_SIZE+map_y,TILE_SIZE, TILE_SIZE))
            if map[row][col] == 9:
                pygame.draw.rect(root,BLUE,(col*TILE_SIZE,row*TILE_SIZE+map_y,TILE_SIZE, TILE_SIZE))
                spawn_placed = True

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
        
    if keys[pygame.K_s]:
        if map_y > -400 * TILE_SIZE + 1080:
            map_y -= 20
    if keys[pygame.K_w]:
        if map_y < 0:
            map_y += 20

    
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
