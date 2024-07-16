#stock data provider
from cachetools import Cache, keys, cached
import pandas as pd
import pathlib

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


def load_history_from_file(data_file):
  data_file = to_history_file_path(data_file)

  if not data_file.exists():
    return pd.DataFrame()

  df = pd.read_parquet(data_file)

  df['day'] = df['day'].apply(
      lambda day: pd.to_datetime(day, format='%Y-%m-%d'))

  def to_float(v):
    try:
      return float(v)
    except:
      return 0.0

  for c in ['open', 'high', 'low', 'close', 'volume']:
    df[c] = df[c].apply(to_float)

  if data_file.as_posix().find('bao_history_') >= 0:
    df['volume'] = df['volume'].apply(lambda v: v / 100.0)

  return df.set_index('day').sort_index()


def save_history_to_file(data_file, df):
  data_file = to_history_file_path(data_file)
  df.to_parquet(data_file, compression='lz4')


def to_history_file_path(data_file):
  if isinstance(data_file, pathlib.Path):
    return data_file.with_suffix('.parquet')

  return pathlib.Path(f'{data_file}').with_suffix('.parquet')


def get_all_history_file_in_path(history_path):
  return history_path.glob('*.parquet')
