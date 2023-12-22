#stock data provider
from cachetools import Cache, keys, cached
import pandas as pd

__local_cache = Cache(maxsize=42)

def __hash_key_for_2(data1, *args):
    return keys.hashkey(id(data1), *args)

@cached(cache=__local_cache, key=__hash_key_for_2)
def create_dataframe(all_data, name='close'):
    trading_data = {}
    for data in all_data:
        trading_data[data.stock_id] = data.data_frame[name]

    panel = pd.DataFrame(data=trading_data)

    return panel.fillna(method='pad')

def filter_dataframe(data, start_date=None, end_date=None):
    if start_date:
        start_date = pd.to_datetime(start_date)
    if end_date:
        end_date = pd.to_datetime(end_date)

    if not start_date and not end_date:
        return data

    if not start_date:
        return data[data.index <= end_date]

    if not end_date:
        return data[data.index >= start_date]

    return data[(data.index >= start_date) & (data.index <= end_date)]
