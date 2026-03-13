import logging
import sys

def setup_logger():
    logger = logging.getLogger()
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        fmt = logging.Formatter(
            fmt='%(asctime)s.%(msecs)03d [%(name)s] %(levelname)s: %(message)s',
            datefmt='%H:%M:%S'
        )

        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(fmt)
        logger.addHandler(handler)
        
    return logger