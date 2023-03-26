import datetime
import json
import os.path
import pathlib
from threading import Lock
from typing import Union

from src import MODULE
__all__ = ['Cache', "Singleton"]

from src.datacache import CACHE_ROOT


class Singleton(type):
    def __init__(self, name, bases, dic):
        super(Singleton, self).__init__(name, bases, dic)
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super(Singleton, self).__call__(*args, **kwargs)
            # cls._instance = cls(*args, **kwargs)  # Error! Lead to call this function recursively
        return self._instance


class Cache(object, metaclass=Singleton):
    """
    """
    FILE = os.path.join(CACHE_ROOT, "search_cache.json")
    KEY_CONTENT = "content"
    KEY_EXPIRE = "expire"
    KEY_TIMESTAMP = "timestamp"
    KEY_ASFILE = "asfile"

    EXPIRE_INSTANT = 0
    EXPIRE_MINUTE = 60
    EXPIRE_MIN5 = 5 * EXPIRE_MINUTE
    EXPIRE_MIN15 = 15 * EXPIRE_MINUTE
    EXPIRE_HOUR = 60 * EXPIRE_MINUTE
    EXPIRE_DAY = 24 * EXPIRE_HOUR
    EXPIRE_WEEK = 7 * EXPIRE_DAY
    EXPIRE_MONTH = 30 * EXPIRE_DAY
    EXPIRE_YEAR = 12 * EXPIRE_MONTH

    def __init__(self):
        self.__wlock = Lock()
        self.content: dict = {}
        pathlib.Path(CACHE_ROOT).mkdir(parents=True, exist_ok=True)
        if os.path.exists(self.FILE):
            with open(self.FILE, "r+") as f:
                self.content: dict = json.load(f)
        else:
            with open(self.FILE, "w+") as f:
                f.write("")

    def get(self, module: str, action: str, key: str, expire=None):
        if info := self.content.get(module, {}).get(action, {}).get(key):
            expire = info[self.KEY_EXPIRE] if expire is None else expire
            if int(datetime.datetime.now().timestamp()) <= info[self.KEY_TIMESTAMP] + expire:
                return self.content[module][action][key][self.KEY_CONTENT]
        return None

    def cache(self, module: str, action: str, key: str, content="", expire=EXPIRE_WEEK) -> Union[None, str]:
        self.__wlock.acquire()
        if result := self.get(module, action, key):
            self.__wlock.release()
            return result
        self.content.setdefault(module, dict())
        self.content[module].setdefault(action, dict())
        self.content[module][action].setdefault(key, dict())
        self.content[module][action][key].update({
            self.KEY_CONTENT: content,
            self.KEY_TIMESTAMP: int(datetime.datetime.now().timestamp()),
            self.KEY_EXPIRE: expire,
            self.KEY_ASFILE: False
        })
        with open(self.FILE, "w+") as f:
            json.dump(self.content, f, indent=2)
        self.__wlock.release()
        return None


if __name__ == "__main__":
    Cache()
    print(Cache().cache(MODULE.STOCK, "PRICE", "0000001"))

