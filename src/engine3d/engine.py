import cv2
import numpy as np
import threading

import renderer
import transforms
import primitives
import camera

class Window:
    def __init__(self):
        self.camera = camera.Camera()

        self.meshes = []
        self.transformed_meshes = []
        self.translations = []
        self.rotations = []
        self.scalings = []
        
        self.width, self.height = 800, 600
        self.frontbuffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.backbuffer = np.zeros_like(self.frontbuffer)

        self.pressed_keys = set()
        self.running = True

        self.lock = threading.Lock()
        self.display_thread = threading.Thread(target=self.display_loop)
        self.display_thread.start()

    def clear(self, colour=(0, 0, 0)):
        self.backbuffer[:, :] = colour

    def put_pixel(self, x, y, colour):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.backbuffer[y, x] = colour
    
    def get_pressed_keys(self):
        return self.pressed_keys
    
    def swap_buffers(self):
        with self.lock:
            self.frontbuffer[:, :] = self.backbuffer
    
    def display_loop(self):
        while self.running:
            with self.lock:
                frame = self.frontbuffer.copy()
            
            cv2.imshow('3D Engine Framebuffer', frame)
            
            key = cv2.waitKey(1)
            if key == 27:
                self.running = False
                break
            elif key != -1:
                self.pressed_keys.add(key)

        cv2.destroyAllWindows()
    
    def update(self):
        self.transformed_meshes[:] = [v @ (t @ r @ s).T for v, t, r, s in zip(self.meshes, self.translations, self.rotations, self.scalings)]

        renderer.render(self, np.concatenate(self.transformed_meshes, axis=0))

        self.pressed_keys.clear()
    
        self.swap_buffers()
        self.clear()

    def add_mesh(self, mesh: np.ndarray=primitives.cube_mesh(), translation: tuple=(0, 0, 0), rotation: tuple=(0, 0, 0), scale: tuple=(1, 1, 1)):
        self.meshes.append(mesh)
        self.translations.append(np.array(transforms.translation_matrix(*translation)))
        self.rotations.append(np.array(transforms.combined_rotation(*rotation), dtype=np.float32))
        self.scalings.append(np.array(transforms.scaling_matrix(*scale), dtype=np.float32))
    
    def translate_object(self, name, idx):
        pass
    
    def rotate_object(self, name, idx):
        pass
    
    def scale_object(self, name, idx):
        pass