# coding=utf-8

import os
import pathlib

import baostock as bs
import pandas as pd
from .path_config import module_path, data_path as g_data_path, vipdoc_path
from stock_data_provider import load_history_from_file, save_history_to_file, to_history_file_path
from .baostock_stock_basic_query import load_stock_info


def convert_symbol(symbol):
  return f'{symbol[:2]}.{symbol[2:]}'


def __load_stock_history(symbol, start_date, end_date):
  rs = bs.query_history_k_data_plus(convert_symbol(symbol),
                                    "date,open,high,low,close,volume",
                                    start_date=start_date,
                                    end_date=end_date,
                                    frequency="d",
                                    adjustflag="3")
  if rs.error_code != '0':
    raise ValueError('baostock query failed:{}, {}'.format(
        rs.error_code, rs.error_msg))

  index_stocks = []
  while (rs.error_code == '0') & rs.next():
    index_stocks.append(rs.get_row_data())

    if rs.error_code != '0':
      raise ValueError('baostock query failed:{}, {}'.format(
          rs.error_code, rs.error_msg))

  result = pd.DataFrame(
      index_stocks, columns=['day', 'open', 'high', 'low', 'close', 'volume'])
  result['day'] = result['day'].apply(
      lambda day: pd.to_datetime(day, format='%Y-%m-%d'))
  result['volume'] = result['volume'].apply(lambda v: float(v) / 100.0)

  return result


def load_all_stock_history(start_date, end_date, data_path=g_data_path):
  pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)
  df = load_stock_info(data_path)

  lg = bs.login()

  if lg.error_code != '0':
    raise ValueError('baostock login failed:{}, {}'.format(
        lg.error_code, lg.error_msg))

  try:
    for idx, row in df.iterrows():
      symbol = row['exchange'] + row['symbol']
      print(symbol)
      if not symbol[:2] in ['sh', 'sz']:
        print(f'skip {symbol}')
        continue

      __download_stock_history(symbol, start_date, end_date)
  finally:
    bs.logout()

def download_stock_history(symbol, start_date, end_date, data_path=g_data_path):
  lg = bs.login()

  if lg.error_code != '0':
    raise ValueError('baostock login failed:{}, {}'.format(
        lg.error_code, lg.error_msg))
  try:
    return __download_stock_history(symbol, start_date, end_date, data_path)
  finally:
    bs.logout()

def __download_stock_history(symbol, start_date, end_date, data_path=g_data_path):
  result = __load_stock_history(symbol, start_date, end_date)

  if result.empty:
    return (False, None)

  start_date = result.head(1)['day'].item().strftime('%Y%m%d')
  end_date = result.tail(1)['day'].item().strftime('%Y%m%d')

  history_path = pathlib.Path(
    data_path
  ) / symbol / f'bao_history_{start_date.replace("-", "")}_{end_date.replace("-", "")}'

  save_history_to_file(history_path, result)

  return (True, load_history_from_file(history_path))


def normalize_history_volume(data_path=g_data_path):
  pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)
  df = load_stock_info(data_path)

  for idx, row in df.iterrows():
    symbol = row['exchange'] + row['symbol']
    print(symbol)

    if not symbol[:2] in ['sh', 'sz']:
      print(f'skip {symbol}')
      continue

    stock_path = pathlib.Path(data_path) / symbol

    history_file_paths = stock_path.glob('bao*.parquet')

    data = []

    for history_file in history_file_paths:
      df = load_history_from_file(history_file)

      data.append(df)

      history_file.unlink()

    if len(data) == 0:
      continue

    all_df = pd.concat(data)

    all_df = all_df.loc[~all_df.index.duplicated(), :].sort_index().reset_index()
    all_df['volume'] = all_df['volume'].apply(lambda v: v / 100.0)

    if all_df.empty:
      continue

    start_date = all_df.head(1)['day'].item().strftime('%Y%m%d')
    end_date = all_df.tail(1)['day'].item().strftime('%Y%m%d')

    history_path = stock_path / f'bao_history_{start_date.replace("-", "")}_{end_date.replace("-", "")}'

    print(history_path)
    save_history_to_file(history_path, all_df)


if __name__ == '__main__':
  data_path = '/home/stone/Work/github/trading_quant/data'
  #load_all_stock_history('2022-01-01', '2024-12-31', data_path)
  #normalize_history_volume(data_path)
