import time
import logging
logging.basicConfig(level=logging.INFO)

class Clock:
    def __init__(self):
        self.last_frame = time.time()
        self.last_delta = 0
    
    def tick(self, FPS):
        delta = time.time() - self.last_frame
        if delta > 1:
            logging.warning(f'\n-     Time      debt    :    {delta:.6f}\n- Debt increased this frame: {delta-self.last_delta:.6f}')
            self.last_delta = float(delta)
        if delta < 1/FPS:
            time.sleep((1/FPS)-delta)
        self.last_frame += 1/FPS