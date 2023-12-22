import logging

from cachetools import Cache, keys, cached
from . import create_dataframe

import talib

__local_cache = Cache(maxsize=42)


def __hash_key_for_2(data1, *args):
    return keys.hashkey(id(data1), *args)

def __MACDHist(*args):
    _, _, macd_hist = talib.MACD(*args)

    return macd_hist

@cached(cache=__local_cache, key=__hash_key_for_2)
def __ref(data, ref_days):
    return data.shift(-ref_days)

def __make_func(func):
    @cached(cache=__local_cache, key=__hash_key_for_2)
    def wrapper(data, *args):
        return data.apply(lambda v: func(v, *args))

    return wrapper

def get_data_globals(data):
    data_globals = {
        'C' : create_dataframe(data, 'close'),
        'O' : create_dataframe(data, 'open'),
        'H' : create_dataframe(data, 'high'),
        'L' : create_dataframe(data, 'low'),
        'V' : create_dataframe(data, 'volume'),
    }

    data_globals['MA'] = __make_func(talib.MA)
    data_globals['MACDHist'] = __make_func(__MACDHist)
    data_globals['RSI'] = __make_func(talib.RSI)
    data_globals['REF'] = __ref
    data_globals['PPO'] = __make_func(talib.PPO)

    return data_globals
