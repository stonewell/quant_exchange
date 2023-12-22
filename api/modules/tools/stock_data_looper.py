# -*- coding: utf-8 -*-
import sys
import os
import time
import random
import logging

from data.hushen300 import hu_shen_300_stocks
from data.zhongxiao import zhongxiao_stocks

class StockDataLooper:
    def __init__(self, _vipdoc_path):
        self.vipdoc_path = _vipdoc_path
        self.hu_shen_300_stocks = hu_shen_300_stocks[:]
        random.seed(time.time())

    def random_hu_shen_300_stocks(self):
        random.shuffle(self.hu_shen_300_stocks)

    def loop_stocks_with_code(self, call_stock, user_info, stock_codes):
        sh_vipdoc_path = os.path.join(self.vipdoc_path, "sh", "lday")
        sz_vipdoc_path = os.path.join(self.vipdoc_path, "sz", "lday")

        for stock_code in stock_codes:
            is_sh = stock_code.upper().startswith('SH')
            is_sz = stock_code.upper().startswith('SZ')

            if is_sh:
                stock_code = stock_code[2:]
            if is_sz:
                stock_code = stock_code[2:]

            stock_data_file = os.path.join(sh_vipdoc_path, ''.join(['sh', str(stock_code), '.day']))
            if os.path.isfile(stock_data_file) and (is_sh or str(stock_code).startswith('60')):
                call_stock(user_info, stock_data_file)
            else:
                stock_data_file = os.path.join(sz_vipdoc_path, ''.join(['sz', str(stock_code), '.day']))
                if os.path.isfile(stock_data_file) and (is_sz or str(stock_code).startswith('0')):
                    call_stock(user_info, stock_data_file)
                else:
                    logging.error('unable to find data file for:{}'.format(stock_code))

    def loop_sh_stocks(self, call_stock, user_info):
        sh_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sh"), "lday")

        for path in os.listdir(sh_vipdoc_path):
            if path.find("sh60") > 0:
                call_stock(user_info, os.path.join(sh_vipdoc_path, path))

    def loop_sh_stocks_range(self, call_stock, user_info, begin, end):
        sh_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sh"), "lday")

        paths = filter(lambda x:x.find("sh60") >= 0, os.listdir(sh_vipdoc_path))

        for i in range(begin, end + 1):
            path = paths[i]
            if path.find("sh60") >= 0:
                call_stock(user_info, os.path.join(sh_vipdoc_path, path))

    def loop_sz_stocks(self, call_stock, user_info):
        sz_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sz"), "lday")

        for path in os.listdir(sz_vipdoc_path):
            if path.find("sz00") > 0:
                call_stock(user_info, os.path.join(sz_vipdoc_path, path))

    def loop_sz_stocks_range(self, call_stock, user_info, begin, end):
        sz_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sz"), "lday")

        paths = filter(lambda x:x.find("sz00") >=0, os.listdir(sz_vipdoc_path))

        for i in range(begin, end + 1):
            path = paths[i]
            if path.find("sz00") >= 0:
                call_stock(user_info, os.path.join(sz_vipdoc_path, path))

    def loop_hu_shen_300_stocks(self, call_stock, user_info):
        sz_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sz"), "lday")
        sh_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sh"), "lday")

        for stock in self.hu_shen_300_stocks:
            path_sh = os.path.join(sh_vipdoc_path, "sh{0}.day".format(stock))
            path_sz = os.path.join(sz_vipdoc_path, "sz{0}.day".format(stock))

            if stock.find("6") == 0 and os.path.exists(path_sh):
                call_stock(user_info, path_sh)
            elif stock.find("0") == 0 and os.path.exists(path_sz):
                call_stock(user_info, path_sz)
            else:
                print('Neither {0} nor {1} is exists!!!!!'.format(path_sh, path_sz))

    def loop_hu_shen_300_stocks_range(self, call_stock, user_info, begin, end):
        sz_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sz"), "lday")
        sh_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sh"), "lday")

        for i in range(begin, end+1):
            stock = self.hu_shen_300_stocks[i]
            path_sh = os.path.join(sh_vipdoc_path, "sh{0}.day".format(stock))
            path_sz = os.path.join(sz_vipdoc_path, "sz{0}.day".format(stock))

            if stock.find("6") == 0 and os.path.exists(path_sh):
                call_stock(user_info, path_sh)
            elif stock.find("0") == 0 and os.path.exists(path_sz):
                call_stock(user_info, path_sz)
            else:
                print('Neither {0} nor {1} is exists!!!!!'.format(path_sh, path_sz))

    def loop_zhongxiao_stocks_range(self, call_stock, user_info, begin, end):
        sz_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sz"), "lday")
        sh_vipdoc_path = os.path.join(os.path.join(self.vipdoc_path, "sh"), "lday")

        for i in range(begin, end+1):
            stock = zhongxiao_stocks[i]
            path_sh = os.path.join(sh_vipdoc_path, "sh{0}.day".format(stock))
            path_sz = os.path.join(sz_vipdoc_path, "sz{0}.day".format(stock))

            if stock.find("6") == 0 and os.path.exists(path_sh):
                call_stock(user_info, path_sh)
            elif stock.find("0") == 0 and os.path.exists(path_sz):
                call_stock(user_info, path_sz)
            else:
                print('Neither {0} nor {1} is exists!!!!!'.format(path_sh, path_sz))
