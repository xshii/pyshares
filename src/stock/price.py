import string
from enum import Enum, auto
from random import choices
from typing import Union, Sequence, Dict, TypeAlias, List

__all__ = ['FREQ', "WEIGHT", "StockPrice"]

import jsonpath as jsonpath
import pandas as pd
import requests as requests

from src import MODULE
from src.datacache.cache import Cache
from src.datacache.store import Store
from src.estmoney.code import WEB, random_token, REQUEST_HEADERS
from src.main import session
from src.stock.cache import StoreSheet
from src.util.logger import logger

code_t: TypeAlias = str

class FREQ(Enum):
    """
    数据的频率
    """
    MIN1 = 1
    MIN5 = 5
    MIN15 = 15
    MIN30 = 30
    MIN60 = 60
    DAILY = 101
    WEEKLY = 102
    MONLY = 103

class WEIGHT(Enum):
    """
    加权方式
    """
    NONE = 0
    FORWARD = 1
    BACKWARD = 2

class DTYPE(Enum):
    PRICE = auto()
    pass


def get(codes: Union[code_t, Sequence[code_t]],
        start='19000101',
        end='20500101',
        freq=FREQ.DAILY,
        weight=WEIGHT.FORWARD,
        dtype=DTYPE.PRICE,
        **kwargs) -> Dict[code_t, pd.DataFrame]:
    if isinstance(codes, code_t):
        codes = [codes]
    if dtype == DTYPE.PRICE:
        return StockPrice.get(codes, start, end, freq, weight, **kwargs)


class CodeType:
    @staticmethod
    def name(code: code_t):
        if not code.startswith("_"):
            code = f"_{code}"
        return code

    @staticmethod
    def origin(code: code_t):
        return code.replace("_", "")


class Stock:

    def __init__(self):
        pass

    @staticmethod
    def __save_name(code: code_t):
        if not code.startswith("_"):
            code = f"_{code}"
        return code

    @staticmethod
    def info(code: code_t):
        url = 'https://searchapi.eastmoney.com/api/suggest/get'
        keyword = code
        params = (
            ('input', f'{keyword}'),
            ('type', '14'),
            ('token', "".join(choices(string.ascii_letters + string.digits, k=32))),
            ('count', f'{1}'),
        )
        json_response = requests.Session().get(url, params=params, timeout=3).json()
        return json_response['QuotationCodeTable']['Data']

    @staticmethod
    def get_id(code: code_t):
        CODE = "Code"
        QCODE = "QuoteID"
        stock_info = Store().load(MODULE.STOCK, StoreSheet.STOCK_INFO)
        result = stock_info.query(f"{CODE} == '{CodeType.name(code)}'", column=QCODE)
        if result is not None:
            return CodeType.origin(result)
        items = Stock.info(code)
        if items is not None:
            if len(items) > 1:
                logger.warn(f"get id len > 1, {items}")
                return None
            items[0][CODE] = CodeType.name(items[0][CODE])
            stock_info.append(items[0])
            stock_info.commit()
            return CodeType.origin(items[0][QCODE])
        return None


class StockPrice:
    FIELDS = [f'f{x}' for x in range(51, 62)]
    COLUMNS = [getattr(WEB, x) for x in FIELDS]

    def __init__(self):
        pass


    @staticmethod
    def _get_single(codes: Union[code_t, Sequence[code_t]],
        start='19000101', end='20500101', freq=FREQ.DAILY, weight=WEIGHT.FORWARD,
        **kwarg):
        pass

    @staticmethod
    def get(codes: code_t,
        start='19000101', end='20500101', freq=FREQ.DAILY, weight=WEIGHT.FORWARD,
        **kwargs) -> Dict[code_t, pd.DataFrame]:
        KLINE_URL = 'https://push2his.eastmoney.com/api/qt/stock/kline/get'
        params = (
            ('fields1', 'f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13'),
            ('fields2', ",".join(StockPrice.FIELDS)),
            ('beg', start),
            ('end', end),
            ('rtntype', '6'),
            ('secid', Stock.get_id(codes)),
            ('klt', f'{freq.value}'),
            ('fqt', f'{weight.value}'),
        )
        json_response = session.get(KLINE_URL, headers=REQUEST_HEADERS, params=params).json()
        klines: List[str] = jsonpath.jsonpath(json_response, '$..klines[:]')
        if not klines:
            return {}
        rows = [x.split(",") for x in klines]
        name = json_response['data']['name']
        dfs = Store().load(MODULE.STOCK, StoreSheet.STOCK_KLINE)
        dic = dict(zip(StockPrice.COLUMNS, rows), Code=[CodeType.name(codes)] * len(rows), name=[name]*len(rows))
        dfs.append(dic)
        dfs.commit()
        return {codes: dfs.df}




if __name__ == "__main__":
    print(Stock.info("000032"))
    print(Stock.get_id("000032"))
