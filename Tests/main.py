from engine3d import Window, cube_mesh, tetrahedron_mesh, Clock

clock = Clock()
window = Window(2000, 1000)

grid_size = 10
for i in range(grid_size):
    for j in range(grid_size):
        window.add_mesh(mesh=tetrahedron_mesh(), translation=(((i-(grid_size//2))*3), ((j-(grid_size//2))*3), grid_size*2))


#window.add_mesh(cube_mesh(), (0, 0, 5))

last_mouse_pos = (0, 0)

angle = 0.1
speed = 1
sensitivity = 0.1
while True:
    mouse_change = (window.mouse_pos[0]-last_mouse_pos[0], window.mouse_pos[1]-last_mouse_pos[1])
    last_mouse_pos = window.mouse_pos
    if window.mouse_down[0]:
        window.camera.yaw += mouse_change[0]*sensitivity
        window.camera.pitch -= mouse_change[1]*sensitivity

    keys = window.get_pressed_keys()
    if ord('w') in keys:
        window.camera.position += window.camera.calculate_looking_direction()*speed
    if ord('s') in keys:
        window.camera.position -= window.camera.calculate_looking_direction()*speed
    if ord('a') in keys:
        window.camera.position += window.camera.calculate_right_direction()*speed
    if ord('d') in keys:
        window.camera.position -= window.camera.calculate_right_direction()*speed

    for i in range(len(window.meshes)):
        window.rotate_object(idx=i, rx=angle/1.23, ry=angle, rz=angle/5.32)

    window.update()
    clock.tick(60)