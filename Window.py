import cv2
import numpy as np
import threading

from Draw import render_mesh

class Window:
    def __init__(self):
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
        self.pressed_keys.clear()
    
        self.swap_buffers()
        self.clear()
