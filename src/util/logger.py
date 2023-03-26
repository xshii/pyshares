import datetime
import logging
import os.path
import pathlib

from src.util import LOG_ROOT
__all__ = ['logger']

logger = logging.getLogger("PyShares")
logger.setLevel(logging.INFO)
path = os.path.join(LOG_ROOT, datetime.datetime.now().strftime("%Y%m%d%H%M%S") + ".txt")
pathlib.Path(LOG_ROOT).mkdir(parents=True, exist_ok=True)
file_handle = logging.FileHandler(path, mode='a')
file_handle.setFormatter('%(asctime)s,%(levelname)s,"%(message)s"')
logger.addHandler(file_handle)

console = logging.StreamHandler()
console.setLevel(logging.INFO)
logger.addHandler(console)
