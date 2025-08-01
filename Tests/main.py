import sys
import os

# Add the parent directory (engine3d/) to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import random

from Environment import Environment
from Camera import Camera
from Mesh import Mesh
from Vector import Vector4
from Clock import Clock

objects = []
for i in range(11):
    for j in range(11):
        objects.append(Mesh.cube())
        objects[-1].position = Vector4((i-5)*3, (j-5)*3, 30)

camera = Camera(
    position=Vector4(0, 0, 0, 1),
    target=Vector4(0, 0, 10000, 1),
    up=Vector4(0, 1, 0, 1),
    fov=90,
    near=0.1,
    far=1000
)

environment = Environment(camera, objects)
clock = Clock()
FPS = 60

while environment.window.running:

    keys = environment.window.get_pressed_keys()

    speed = 1
    if ord('w') in keys:
        camera.position.z += speed
    if ord('s') in keys:
        camera.position.z -= speed
    if ord('a') in keys:
        camera.position.x += speed
    if ord('d') in keys:
        camera.position.x -= speed
    
    objects[0].rotate(0.022, 0.037)

    clock.tick(FPS)
    environment.update()