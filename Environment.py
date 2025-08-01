from Window import Window
from Camera import Camera
from Draw import render_mesh

class Environment:
    def __init__(self, camera=None, objects=[]):
        self.window = Window()
        if camera is None:
            self.camera = Camera()
        elif camera.aspect_ratio is None:
            camera.aspect_ratio = self.window.width/self.window.height
            self.camera = camera
        else:
            self.camera = camera
        self.objects = objects
    
    def update(self):
        self.window.update()

        for mesh in self.objects:
            render_mesh(self.window, mesh, self.camera)
