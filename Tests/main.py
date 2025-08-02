if __name__ == '__main__':
    import sys
    import os

    # Add the parent directory (engine3d/) to sys.path
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

    from Environment import Environment
    from Camera import Camera
    from Mesh import Mesh
    from Clock import Clock
    import numpy as np

    objects = []
    objects.append(Mesh.cube())
    objects.append(Mesh.tetrahedron())
    objects[-1].position = np.array([5, 0, 0, 1], dtype=np.float32)

    camera = Camera(
        position=np.array([0, 0, -5, 1], dtype=np.float32),
        target=np.array([0, 0, 10000, 1], dtype=np.float32),
        up=np.array([0, 1, 0, 0], dtype=np.float32),
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
        
        objects[0].rotate(0.022, 0.037)

        clock.tick(FPS)
        environment.update()