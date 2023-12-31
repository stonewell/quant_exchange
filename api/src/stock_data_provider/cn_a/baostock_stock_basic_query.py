# coding=utf-8

import os
import csv
import pathlib

import baostock as bs
import pandas as pd
from .path_config import module_path, data_path as g_data_path, vipdoc_path


def convert_symbol(symbol):
  parts = symbol.lower().split('.')

  return '{}{}'.format(parts[0], parts[1])


def get_symbol(symbol):
  parts = symbol.lower().split('.')

  return '{}{}'.format(parts[0], parts[1])


def load_stocks_from_file(data_file):
  df = pd.read_csv(data_file)

  df['symbol'] = df['code'].apply(lambda code: code.lower().split('.')[1])
  df['exchange'] = df['code'].apply(lambda code: code.lower().split('.')[0])

  return df[df['status'] == 1]


def load_stock_info(data_path=g_data_path):
  data_file = os.path.join(data_path, 'stocks.csv')

  if os.path.exists(data_file):
    return load_stocks_from_file(data_file)

  lg = bs.login()

  if lg.error_code != '0':
    raise ValueError('baostock login failed:{}, {}'.format(
        lg.error_code, lg.error_msg))

  try:
    rs = bs.query_stock_basic()
    if rs.error_code != '0':
      raise ValueError('baostock query failed:{}, {}'.format(
          rs.error_code, rs.error_msg))

    index_stocks = []
    while (rs.error_code == '0') & rs.next():
      index_stocks.append(rs.get_row_data())

      if rs.error_code != '0':
        raise ValueError('baostock query failed:{}, {}'.format(
            rs.error_code, rs.error_msg))

    result = pd.DataFrame(index_stocks, columns=rs.fields)

    pathlib.Path(data_path).mkdir(parents=True, exist_ok=True)

    result.to_csv(data_file, encoding="utf-8", index=False)

    return load_stocks_from_file(data_file)
  finally:
    bs.logout()


if __name__ == '__main__':
  data_path = '/home/stone/Work/github/trading_quant/data'
  print(load_stock_info(data_path))
