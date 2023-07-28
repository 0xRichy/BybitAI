import logging
import numpy as np

class IndicatorGenerator:
    def generate_ai_indicator(self, data):
        ema_period = 12
        ema = np.mean(data[-ema_period:])
        logging.info(f"AI indicator generated: {ema} at {time.time()}")
        return ema
