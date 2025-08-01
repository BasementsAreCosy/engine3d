import time
import logging
logging.basicConfig(level=logging.INFO)

class Clock:
    def __init__(self):
        self.last_frame = time.time()
    
    def tick(self, FPS):
        delta = time.time() - self.last_frame
        #logging.info(f'Time debt: {delta}')
        if delta < 1/FPS:
            time.sleep((1/FPS)-delta)
        self.last_frame += 1/FPS