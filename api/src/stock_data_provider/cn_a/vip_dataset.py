import sys
import os
import logging

from .path_config import module_path, data_path, vipdoc_path
import data.data_loader
from tools.stock_data_looper import StockDataLooper

import pandas as pd
import datetime
import numpy

from . import baostock_adjfactor as adj

class VipDataSet(object):
    def __init__(self, stock_id, do_normalize_data):
        self.err = False
        self.stock_id = stock_id
        self.data_frame = pd.DataFrame(columns=['day', 'open', 'high', 'low', 'close', 'volume'])
        self.data_frame.set_index('day')
        self.holidays = None
        self.trading_date = None
        self.do_normalize_data = do_normalize_data

def process_stock_file(userinfo, stock_data_file):
    data_frame = []
    stock_id = os.path.splitext(os.path.basename(stock_data_file))[0]
    tushare_symbol = '{}.{}'.format(stock_id[2:], stock_id[:2].upper())

    logging.info('processing {}, id:{}'.format(stock_data_file, stock_id))

    try:
        with open(stock_data_file,'rb') as f:
            trading_date = []
            while True:
                d = data.data_loader.read_next_day_data(f)

                if d == None:
                    break
                day = pd.to_datetime(d.date, format='%Y%m%d')
                data_frame.append({'day':day,
                                   'open':d.open_price / 100,
                                   'high':d.highest_price / 100,
                                   'low':d.lowest_price / 100,
                                   'close':d.close_price / 100,
                                   'volume':d.vol})
                trading_date.append(day.tz_localize('UTC'))
            #end while

            data_frame = pd.DataFrame(data=data_frame,
                                      columns=['day', 'open', 'high', 'low', 'close', 'volume'])
            data_frame = data_frame.set_index('day').sort_index()

            userinfo.data_frame = data_frame
            userinfo.err = False
            dr = pd.date_range(start=trading_date[0], end=trading_date[-1])

            if userinfo.do_normalize_data:
                normalize_data(userinfo, tushare_symbol)
            userinfo.holidays = list(map(pd.to_datetime, numpy.setdiff1d(dr, pd.DatetimeIndex(trading_date))))
            userinfo.trading_date = trading_date
        #end with
    except:
        userinfo.err = True
        logging.exception('Error process:{}'.format(stock_data_file))


def normalize_data(vip_data, tushare_symbol):
    s_data_path = os.path.normpath(os.path.join(data_path, tushare_symbol))

    os.makedirs(s_data_path, exist_ok=True)

    values = adj.load_adjfactor(tushare_symbol, data_path)

    def adj_price(x, *args, **kwds):
        try:
            adj_v = adj.get_adjv_for_date(values, x.name)
            v = [x['open'] * adj_v,
                    x['high'] * adj_v,
                    x['low'] * adj_v,
                    x['close'] * adj_v,
                    x['volume']]

            return v
        except KeyError:
            return x
        except:
            logging.exception('Error adj prices')
            return x

    vip_data.data_frame = vip_data.data_frame.apply(adj_price, result_type='broadcast', axis=1)

def __load_stock_data(symbol, do_normalize_data = True):
    symbol = symbol.strip()

    stock_data_looper = StockDataLooper(vipdoc_path)

    data = VipDataSet(symbol, do_normalize_data)

    stock_data_looper.loop_stocks_with_code(process_stock_file,
                                            data,
                                            [symbol])

    if data.err:
        raise ValueError()

    return data

def load_stock_data(symbol, do_normalize_data = True):
    symbols = symbol.split(',')

    if len(symbols) == 0:
        raise ValueError('no symbol:%s' % symbol)

    return list(map(lambda x: __load_stock_data(x, do_normalize_data), symbols))
