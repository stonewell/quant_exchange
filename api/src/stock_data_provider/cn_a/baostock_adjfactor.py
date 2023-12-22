# coding=utf-8

import os
import csv

import baostock as bs
import pandas as pd


def convert_symbol(symbol):
    parts = symbol.lower().split('.')

    return '{}.{}'.format(parts[1], parts[0])


def load_adjfactor(symbol, data_path):
    adj_file = os.path.join(data_path, symbol, 'adj.csv')

    if os.path.exists(adj_file):
        return load_adjfactor_from_file(adj_file)

    lg = bs.login('anonymous', '123456')

    if lg.error_code != '0':
        raise ValueError('baostock login failed:{}, {}'.format(lg.error_code, lg.error_msg))

    rs_list = []
    rs_factor = bs.query_adjust_factor(convert_symbol(symbol), start_date="1990-01-01", end_date="2199-12-31")
    while (rs_factor.error_code == '0') & rs_factor.next():
        rs_list.append(rs_factor.get_row_data())

        if rs_factor.error_code != '0':
            bs.logout()
            raise ValueError('baostock read data failed:{}'.format(rs_factor.error_msg))

    bs.logout()

    result_factor = pd.DataFrame(rs_list, columns=rs_factor.fields)

    result_factor.to_csv(adj_file, encoding="utf-8", index=False)

    return load_adjfactor_from_file(adj_file)


def load_adjfactor_from_file(adj_file):
    values = {}

    with open(adj_file, 'r') as f:
        reader = csv.DictReader(f)
        for line in reader:
            values[pd.to_datetime(line['dividOperateDate'])] = float(line['backAdjustFactor'])
        # end for
    # end with

    return values


def get_adjv_for_date(values, d):
    dates = sorted(values.keys())

    try:
        for i in range(len(dates)):
            if d < dates[i]:
                return values[dates[i - 1]] if i > 0 else values[dates[0]]

        return values[dates[-1]]
    except:
        raise KeyError

if __name__ == '__main__':
    values = load_adjfactor('600019.SH', 'data')
    print(values)
