# -*- coding: utf-8 -*-
import sys
import os
from traceback import print_exception
from math import fsum
import pickle

from stutils.k_means import k_means

class KLineStockModel:
    def __init__(self):
        self.categories = {}
        self.category_values = {}
        self.category_bars = {}

    def update(self):
        for category in self.categories.keys():
            category_day = {}
            self.category_values[category] = category_day

            for day in self.categories[category].keys():
                total = fsum(self.categories[category][day].values())
                features = self.categories[category][day].keys()
                category_day[day] = {feature : self.categories[category][day][feature] / total for feature in features}
            #end for day
        #end for category

    def train_line(self, data_line):
        parts = data_line.split(' ')
        assert len(parts) > 0

        category = int(parts[0])
        assert category >= 0 and category <= 9

        return self.calc_line_value(category, ' '.join(parts[1:]))

    def predict_line(self, data_line):
        predict_result = {}
        for category in self.categories.keys():
            predict_result[category] = 0
            
            if not self.category_bars.has_key(category):
                continue
            
            v = self.calc_line_value(category, data_line)
            category_bar = self.category_bars[category][0]
            max_category_bar = self.category_bars[category][1]
            min_category_bar = self.category_bars[category][2]

            if v > max_category_bar or v < min_category_bar:
                continue
            
            bar_count_sum = fsum(category_bar.values())
            category_bar_keys = category_bar.keys()

            min = abs(v - category_bar_keys[0])
            result_bar = 0
            
            for i in range(1, len(category_bar_keys)):
                delta = abs(v - category_bar_keys[i])
                if min > delta:
                    min = delta;
                    result_bar = i
                #end if
            #end for

            predict_result[category] = category_bar[category_bar_keys[result_bar]] / bar_count_sum
        #end for

        return predict_result

    def calc_line_value(self, category, line):
        assert self.categories.has_key(category)
        model_category_value = self.category_values[category]

        parts = line.split(' ')

        result = 0.0

        for i in range(0, len(parts)):
            sub_parts = parts[i].split(':')
            if (len(sub_parts) != 2):
                continue

            day = int(sub_parts[0])
            k_line = int(sub_parts[1])

            category_day_value = {}
            if (model_category_value.has_key(day)):
                category_day_value = model_category_value[day]
            else:
                continue

            if (category_day_value.has_key(k_line)):
                result += category_day_value[k_line]
            else:
                continue
        #end for i in range

        return result

    def store_to_file(self, model_file_path):
        f = open(model_file_path, "wb")
        pickle.dump(self.categories, f)
        pickle.dump(self.category_values, f)
        pickle.dump(self.category_bars, f)
        f.close()

    def load_from_file(self, model_file_path):
        f = open(model_file_path)
        self.categories = pickle.load(f)
        self.category_values = pickle.load(f)
        self.category_bars = pickle.load(f)
        f.close()

    def update_category_bars(self, category_values):
        self.category_bars = {}
        for category in category_values.keys():
            data = category_values[category]
            self.category_bars[category] = [k_means(data, 3), max(data), min(data)]
    #end def 
