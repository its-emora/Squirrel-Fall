# What is this project?

This project is something I am working on as a part of Hackclub Flavortown. My aim is for this project to allow me to gain experience in coding with PyGame and vector-based movement. 


# The Game Premise

The game will be a simple dropper/platformer style. The player will play as a flying squirrel and is tasked with making their way down a thick jungle tower in the shortest time possible.


# Where are we now?

The game has basic vector based movement with gravity. The player can move left and right using the A and D keys. Once the player leaves the screen. they are tansported to the other side of the screen. The player sprite moves both left and right corrispondingly. 

Vectors have an overall multiplier so if you hold down both A and D simultaneously, the player will not move.

The tilemap now loads. 0 = air; 1 = dirt; 9 = Player spawn. The tilemap has collisions. You can land on a platform and walk off it. If you hit a platform from the side it will not teleport you ontop of it.


# Plans for the future

Next I will be adding a jump funtion to make it easier to traverse the terrian. I am also looking at making a map builder program to allow for easier map building. 
