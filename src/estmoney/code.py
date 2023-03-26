import dataclasses
import random
import string

import pandas as pd

MARKET_DF = pd.DataFrame(columns=['id', 'market'], data=[
    [0, 'shenzhen'],
    [1, "shanghai"],
    [105, "us"],
    [106, "us"],
    [107, "us"],
    [116, "hongkong"],
    [128, "hongkong"],
    [113, "上期所"],
    [114, '大商所'],
    [115, '郑商所'],
    [8, '中金所'],
    [142, '上海能源期货交易所'],
    [155, '英股'],
    [90, '板块'],
    [225, '广期所'],
])


@dataclasses.dataclass(frozen=True)
class WEB:
    f2: str = "now"      # 最新价
    f3: str = "raise_drop_rate"  # 涨跌幅
    f4: str = "raise_drop_price"     # 涨跌额
    f5: str = "deal_number"      # 成交量
    f6: str = "deal_volumn"       # 成交额
    f8: str = "hand_over_rate"       # 换手率
    f9: str = "dynamic_pe"       # 动态市盈率
    f10: str = "amount_ratio"             # 量比
    f12: str = "code"    # 代码
    f13: str = "market_id"   # 市场编号
    f14: str = "name"    # 名称
    f15: str = 'max'     # 最高
    f16: str = 'min'     # 最低
    f17: str = 'begin'     # 开盘
    f18: str = "last_day_end"    # 昨日收盘
    f20: str = "ev"        # 企业市值 enterpice value
    f21: str = "trade_ev"        # 流通市值
    f51: str = "date"    # 日期
    f52: str = 'begin'   # 开盘
    f53: str = "end"     # 收盘
    f54: str = "max"     # 最高
    f55: str = "min"     # 最低
    f56: str = "deal_number"     # 成交量
    f57: str = "deal_volumn"      # 成交额
    f58: str = "viber_rate"        # 振幅
    f59: str = "raise_drop_rate"    # 涨跌幅
    f60: str = "raise_drop_price"    # 涨跌额
    f61: str = "hand_over_rate"    # 涨跌幅
    f105: str = "net_profit" # 净利润
    f124: str = "timestamp"  # 更新时间戳
    f173: str = "roe"
    f186: str = "gross_profit_rate"  # 毛利率
    f187: str = "net_profit_rate"    # 净利率
    f297: str = "new_trade_day"  # 最新交易日

    def as_dict(self):
        return dataclasses.asdict(self)

REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.2 Safari/605.1.15',
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.3,en;q=0.9',
}


def random_token():
    return "".join(random.choices(string.ascii_letters + string.digits, k=32))


if __name__ == "__main__":
    w = getattr(WEB, "f51")
    print(w)
