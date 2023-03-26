import datetime
import os.path
import pathlib
from collections import defaultdict

__all__ = ['Store']

from typing import Union

import pandas as pd

from src.datacache import DATA_ROOT
from src.datacache.cache import Singleton
from src.util.logger import logger


KEY_TIMESTAMP = "timestamp"


class PdStore:
    def __init__(self, module, sheet):
        self.mod = module
        self.sheet = sheet
        self._df: Union[pd.DataFrame, None] = None


    @property
    def df(self):
        return self._df

    def query(self, expression: str, column: Union[str, None] = None, length=1):
        try:
            if column is None:
                column = self._df.columns
            if length == 1:
                return self.df.query(expression).iloc[0][column]
            return self.df.query(expression).iloc[:length, column]
        except:
            return None

    def load(self) -> Union[pd.DataFrame, None]:
        if self._df is not None:
            return self._df
        try:
            self._df = pd.read_csv(self.__path)
            return self._df
        except FileNotFoundError:
            logger.info(f"正在创建{self.__path}")
            self._df = pd.DataFrame()
            return self._df
        except Exception as e:
            logger.warning(f"创建失败{e.__repr__()}")
            return None

    @property
    def __path(self):
        return os.path.join(DATA_ROOT, self.mod, self.sheet) + ".csv"

    @staticmethod
    def timestamp(length=0):
        if length == 0:
            return {Store.KEY_TIMESTAMP: int(datetime.datetime.now().timestamp())}
        return {Store.KEY_TIMESTAMP: [int(datetime.datetime.now().timestamp())] * length}

    def append(self, outer: Union[dict, pd.DataFrame], **kwargs):
        if isinstance(outer, dict) and len(outer) > 0:
            length = 1
            if isinstance(outer[list(outer.keys())[0]], list):
                length = len(outer[list(outer.keys())[0]])
            outer.update(self.timestamp(length))
            outer = pd.DataFrame(outer, index=range(length), **kwargs)
        self._df = pd.concat([self._df, outer])

    def commit(self):
        if self._df is None:
            logger.warning(f"{self.mod}, {self.sheet} nothing to save")
            return
        pathlib.Path(os.path.dirname(self.__path)).mkdir(parents=True, exist_ok=True)
        self._df.to_csv(self.__path, index=False)


class Store(object, metaclass=Singleton):
    """
    """
    KEY_PD = "pd"
    KEY_TIMESTAMP = "timestamp"

    def __init__(self):
        self._loaded = defaultdict(lambda: defaultdict(dict))
        pass

    def load(self, module: str, sheet: str) -> PdStore:
        if len(self._loaded[module][sheet]) == 0:
            pds = PdStore(module, sheet)
            pds.load()
            self._loaded[module][sheet].update({self.KEY_PD: pds})
        return self._loaded[module][sheet][self.KEY_PD]

    def dump(self, module, sheet):
        dfs = self._loaded[module][sheet].get(self.KEY_PD, None)     # type: PdStore
        if dfs is None:
            logger.warning("未加载过的文件")
            return
        dfs.commit()
