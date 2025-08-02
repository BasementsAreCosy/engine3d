import sys
import os

# Add the parent directory (engine3d/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Environment import Environment
from Camera import Camera
from Mesh import Mesh
from Clock import Clock
import numpy as np
from HelperFunctions import vector4

objects = []
grid_size = 1
for i in range(grid_size):
    for j in range(grid_size):
        objects.append(Mesh.cube())
        objects[-1].position = vector4((i-((grid_size-1)/2))*5, (j-((grid_size-1)/2))*5, 30, 1)

camera = Camera(
    position=vector4(0, 0, 0, 1),
    target=vector4(0, 0, 10000, 1),
    up=vector4(0, 1, 0, 0),
    fov=90,
    near=0.1,
    far=1000
)

environment = Environment(camera, objects)
clock = Clock()
FPS = 60

while environment.window.running:

    keys = environment.window.get_pressed_keys()

    speed = 0.2
    if ord('w') in keys:
        camera.position[2] += speed
    if ord('s') in keys:
        camera.position[2] -= speed
    if ord('a') in keys:
        camera.position[0] += speed
    if ord('d') in keys:
        camera.position[0] -= speed
    
    #objects[0].rotate(0.022, 0.037)

    clock.tick(FPS)
    environment.update()