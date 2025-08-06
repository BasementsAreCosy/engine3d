from engine3d import Window, cube_mesh, Clock

clock = Clock()
window = Window(2000, 1000)

grid_size = 40
for i in range(grid_size):
    for j in range(grid_size):
        window.add_mesh(mesh=cube_mesh(), translation=(((i-(grid_size//2))*5), ((j-(grid_size//2))*5), grid_size*3))


#window.add_mesh(cube_mesh(), (0, 0, 5))

angle = 0.1
speed = 0.1
while True:
    keys = window.get_pressed_keys()
    if ord('w') in keys:
        window.camera.position.z += speed
    if ord('s') in keys:
        window.camera.position.z -= speed
    if ord('a') in keys:
        window.camera.position.x += speed
    if ord('d') in keys:
        window.camera.position.x -= speed

    for i in range(len(window.meshes)):
        window.rotate_object(idx=i, rx=angle/1.23, ry=angle, rz=angle/5.32)

    window.update()
    clock.tick(10)