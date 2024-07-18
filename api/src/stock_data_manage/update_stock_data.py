from stock_data_provider.cn_a.vip_dataset import load_stock_data_with_vipdoc_path
from stock_data_provider.cn_a.path_config import data_path as g_data_path
from stock_data_provider.cn_a import load_stock_data, load_stock_info
from stock_data_provider import load_history_from_file, save_history_to_file

import pandas as pd
import pathlib


def load_vipdata(symbol, _vipdata_path):
  d = load_stock_data_with_vipdoc_path(symbol, _vipdata_path, False)

  return d[0].data_frame


def merge_stock_data(symbol, _data_path, vipdoc_path_list):
  data_path = pathlib.Path(_data_path) / symbol
  data_path.mkdir(parents=True, exist_ok=True)

  history_path = data_path / 'history.parquet'

  cur_df = load_history_from_file(history_path)

  data_sets = []

  if not cur_df.empty:
    print(cur_df)
    data_sets.append(cur_df)

  for vipdoc_path in vipdoc_path_list:
    _df = load_vipdata(symbol, vipdoc_path)
    if not _df.empty:
      print(_df)
      data_sets.append(_df)

  if len(data_sets) == 0:
    print(f'no data for {symbol}')
    return

  all_df = pd.concat(data_sets)

  all_df = all_df.loc[~all_df.index.duplicated(), :].reset_index()

  save_history_to_file(history_path, all_df)


def merge_vipdoc_data():
  df = load_stock_info()

  # merge_stock_data(
  #      'sh600019', g_data_path,
  #      ['/media/share/win/vipdoc', '/media/share/win/vipdoc_2015_2022'])
  # raise ValueError()
  for idx, row in df.iterrows():
    print(row['exchange'] + row['symbol'])
    merge_stock_data(
        row['exchange'] + row['symbol'], g_data_path,
        ['/media/share/win/vipdoc', '/media/share/win/vipdoc_2015_2022'])

if __name__ == '__main__':
  pass
