from engine3d import Window, cube, Clock

clock = Clock()
window = Window()

grid_size = 11
for i in range(grid_size):
    for j in range(grid_size):
        window.add_mesh(cube(), (((i-(grid_size//2))*5), ((j-(grid_size//2))*5), 30))

angle = 0.07
while True:
    window.update()
    
    #for i in range(len(window.rotations)):
    #    window.rotations[i] = window.rotation_all(angle/1.23, angle, angle/5.32)

    angle += 0.05

    clock.tick(60)