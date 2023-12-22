# coding=utf-8

import os
import csv
import pathlib

import baostock as bs
import pandas as pd


def convert_symbol(symbol):
    parts = symbol.lower().split('.')

    return '{}{}'.format(parts[0], parts[1])

def load_stocks_from_file(data_file):
  values = {}

  with open(data_file, 'r') as f:
    reader = csv.DictReader(f)
    for line in reader:
      values[convert_symbol(line['code'])] = line['code_name']
    # end for
  # end with

  return values

def load_index(index, query_func, data_path):
  data_file = os.path.join(data_path, index, 'stocks.csv')

  if os.path.exists(data_file):
    return load_stocks_from_file(data_file)

  lg = bs.login()

  if lg.error_code != '0':
    raise ValueError('baostock login failed:{}, {}'.format(lg.error_code, lg.error_msg))

  try:
    rs = query_func()
    if rs.error_code != '0':
      raise ValueError('baostock query {} failed:{}, {}'.format(index, rs.error_code, rs.error_msg))

    index_stocks = []
    while (rs.error_code == '0') & rs.next():
      index_stocks.append(rs.get_row_data())

      if rs.error_code != '0':
        raise ValueError('baostock query {} failed:{}, {}'.format(index, rs.error_code, rs.error_msg))

      result = pd.DataFrame(index_stocks, columns=rs.fields)

      pathlib.Path(os.path.join(data_path, index)).mkdir(parents=True, exist_ok=True)

      result.to_csv(data_file, encoding="utf-8", index=False)

      return load_stocks_from_file(data_file)
  finally:
    bs.logout()

def load_all_indexes(data_path):
  indexes = {}

  indexes['hs300'] =load_index('hs300', bs.query_hs300_stocks, data_path)
  indexes['sz50'] =load_index('sz50', bs.query_sz50_stocks, data_path)
  indexes['zz500'] =load_index('zz500', bs.query_zz500_stocks, data_path)

  return indexes

if __name__ == '__main__':
  print(load_all_indexes('data'))
