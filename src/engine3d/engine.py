import cv2
import numpy as np
import threading

from . import renderer
from . import transforms
from . import primitives
from . import camera

class Window:
    def __init__(self, width=800, height=600):
        self.mesh_references = {}
        self.meshes = []
        self.transformed_meshes = []
        self.translation_matrices = []
        self.translation_raw = []
        self.rotation_matrices = []
        self.rotation_raw = []
        self.scaling_matrices = []
        self.scaling_raw = []
        
        self.width, self.height = width, height
        self.frontbuffer = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        self.backbuffer = np.zeros_like(self.frontbuffer)

        self.camera = camera.Camera(aspect_ratio=self.width/self.height)

        self.mouse_pos = (0, 0)
        self.mouse_down = [False, False, False] # left, middle, right
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
        with self.lock:
            return self.pressed_keys
    
    def swap_buffers(self):
        with self.lock:
            self.frontbuffer[:, :] = self.backbuffer
    
    def display_loop(self):
        cv2.namedWindow('3D Engine Framebuffer')
        cv2.setMouseCallback('3D Engine Framebuffer', self.mouse_callback)
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
    
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_MOUSEMOVE:
            self.mouse_pos = (x, y)

        elif event == cv2.EVENT_LBUTTONDOWN:
            self.mouse_down[0] = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.mouse_down[0] = False
        
        elif event == cv2.EVENT_MBUTTONDOWN:
            self.mouse_down[1] = True
        elif event == cv2.EVENT_MBUTTONUP:
            self.mouse_down[1] = False
        
        elif event == cv2.EVENT_RBUTTONDOWN:
            self.mouse_down[2] = True
        elif event == cv2.EVENT_RBUTTONUP:
            self.mouse_down[2] = False
    
    def update(self):
        self.transformed_meshes[:] = [v @ (t @ r @ s).T for v, t, r, s in zip(self.meshes, self.translation_matrices, self.rotation_matrices, self.scaling_matrices)]

        renderer.render(self, np.concatenate(self.transformed_meshes, axis=0))

        self.pressed_keys.clear()
    
        self.swap_buffers()
        self.clear()

    def add_mesh(self, name: str=None, mesh: np.ndarray=primitives.cube_mesh(), translation: list=None, rotation: list=None, scale: list=None):
        if translation is None:
            translation = [0, 0, 0]
        if rotation is None:
            rotation = [0, 0, 0]
        if scale is None:
            scale = [1, 1, 1]

        if name is None:
            name = f'Object {len(self.meshes)}'
        self.mesh_references[name] = len(self.meshes)
        self.meshes.append(mesh)
        self.translation_matrices.append(np.array(transforms.translation_matrix(*translation), dtype=np.float32))
        self.translation_raw.append(translation)
        self.rotation_matrices.append(np.array(transforms.combined_rotation_matrix(*rotation), dtype=np.float32))
        self.rotation_raw.append(rotation)
        self.scaling_matrices.append(np.array(transforms.scaling_matrix(*scale), dtype=np.float32))
        self.scaling_raw.append(scale)

    def translate_object(self, name=None, idx=None, tx=0, ty=0, tz=0):
        idx = self.get_index(name, idx)
        if idx is None:
            return
        self.translation_raw[idx][0] += tx
        self.translation_raw[idx][1] += ty
        self.translation_raw[idx][2] += tz
        self.translation_matrices[idx] = np.array(transforms.translation_matrix(*self.translation_raw[idx]), dtype=np.float32)
    
    def rotate_object(self, name=None, idx=None, rx=0, ry=0, rz=0):
        idx = self.get_index(name, idx)
        if idx is None:
            return
        self.rotation_raw[idx][0] += rx
        self.rotation_raw[idx][1] += ry
        self.rotation_raw[idx][2] += rz
        self.rotation_matrices[idx] = np.array(transforms.combined_rotation_matrix(*self.rotation_raw[idx]), dtype=np.float32)
    
    def scale_object(self, name=None, idx=None, sx=0, sy=0, sz=0):
        idx = self.get_index(name, idx)
        if idx is None:
            return
        self.scaling_raw[idx][0] += sx
        self.scaling_raw[idx][1] += sy
        self.scaling_raw[idx][2] += sz
        self.scaling_matrices[idx] = np.array(transforms.scaling_matrix(*self.scaling_raw[idx]), dtype=np.float32)

    def set_object_translation(self, name=None, idx=None, tx=None, ty=None, tz=None):
        idx = self.get_index(name, idx)
        if idx is None:
            return
        if not (tx is None):
            self.translation_raw[idx][0] = tx
        if not (ty is None):
            self.translation_raw[idx][1] = ty
        if not (tz is None):
            self.translation_raw[idx][2] = tz
        self.translation_matrices[idx] = np.array(transforms.translation_matrix(tx, ty, tz), dtype=np.float32)
    
    def set_object_rotation(self, name=None, idx=None, rx=None, ry=None, rz=None):
        idx = self.get_index(name, idx)
        if idx is None:
            return
        if not (rx is None):
            self.rotation_raw[idx][0] = rx
        if not (ry is None):
            self.rotation_raw[idx][1] = ry
        if not (rz is None):
            self.rotation_raw[idx][2] = rz
        self.rotation_matrices[idx] = np.array(transforms.combined_rotation_matrix(rx, ry, rz), dtype=np.float32)
    
    def set_object_scale(self, name=None, idx=None, sx=None, sy=None, sz=None):
        idx = self.get_index(name, idx)
        if idx is None:
            return
        if not (sx is None):
            self.scaling_raw[idx][0] = sx
        if not (sy is None):
            self.scaling_raw[idx][1] = sy
        if not (sz is None):
            self.scaling_raw[idx][2] = sz
        self.scaling_matrices[idx] = np.array(transforms.scaling_matrix(sx, sy, sz), dtype=np.float32)
        

    def get_index(self, name, idx):
        if not (name is None):
            if name in self.mesh_references.keys():
                idx = self.mesh_references[name]
            else:
                return None
        elif idx is None:
            return None
        return idx