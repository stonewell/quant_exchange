from __future__ import print_function
import sys
import os
import shutil

from time import strftime,localtime

import svm_generator
import svm_nodes_creator
import svm_tools
import data.data_loader

class StockSVM(object):
    def __init__(self, stock_data_file, stock_svm_path, svm_bin_path,
                 nodes_creator = svm_nodes_creator.create_nodes_1,
                 use_amount = True,
                 look_back_days = 10,
                 predict_days = 5,
                 update_model = True,
                 update_predict = True,
                 forward_days = 2,
                 filter_zero = False,
                 output_day = True,
                 nodes_names = None):
        self.stock_data_file = stock_data_file
        self.stock_svm_path = stock_svm_path
        self.model_history_path = os.path.join(stock_svm_path, "models")
        self.model_file = self.gen_model_file_name()
        self.svm_tmp_path = os.path.join(stock_svm_path, "tmp")
        self.predict_history_path = os.path.join(stock_svm_path, "predicts")
        self.predict_file = self.gen_predict_file_name(self.stock_data_file)
        self.svm_bin_path = svm_bin_path

        self.look_back_days = look_back_days
        self.predict_days = predict_days
        
        self.generator = svm_generator.SVMGenerator(nodes_creator,
                                                     look_back_days = look_back_days,
                                                     predict_days = predict_days,
                                                     use_amount = use_amount,
                                                     filter_zero = filter_zero,
                                                     output_day = output_day,
                                                     nodes_names = nodes_names)
        self.svm_tools = svm_tools.SvmTools(self.svm_bin_path)

        self.update_model = update_model
        self.update_predict = update_predict
        self.forward_days = forward_days
        self.filter_zero = filter_zero
        
        #make sure all path exists
        self.make_sure_path_exists()

        #backup old model and generate new if needed
        if update_model:
            self.backup_and_gen_model()

        #backup old predict and generate new if needed
        if update_predict:
            self.backup_and_gen_predict()

    def gen_model_file_name(self):
        file_part = os.path.basename(os.path.splitext(self.stock_data_file)[0])

        return file_part + "_" + "model_" + strftime("%Y", localtime())

    def gen_predict_file_name(self, stock_data_file):
        file_part = os.path.basename(os.path.splitext(stock_data_file)[0])

        return file_part + "_" + "predict_" + strftime("%Y", localtime())

    def create_path_if_need(self, path):
        if os.path.isdir(path):
            return

        os.makedirs(path)
        
    def make_sure_path_exists(self):
        self.create_path_if_need(self.stock_svm_path)
        self.create_path_if_need(self.model_history_path)
        self.create_path_if_need(self.svm_tmp_path)
        self.create_path_if_need(self.predict_history_path)

    def backup_and_gen_model(self):
        file_prefix = os.path.basename(os.path.splitext(self.stock_data_file)[0])

        file_prefix = file_prefix + "_" + "model_"

        has_current = False
        for path in os.listdir(self.stock_svm_path):
            if path.startswith(file_prefix) and not path.startswith(self.model_file):
                shutil.move(os.path.join(self.stock_svm_path, path),
                            os.path.join(self.model_history_path, path))

            if path.startswith(self.model_file):
                has_current = True

        if not has_current:
            self._svm_model_gen()

    def clear_tmp_path(self):
        shutil.rmtree(self.svm_tmp_path, True)
        self.make_sure_path_exists()
        
    def clear_model_path(self):
        shutil.rmtree(self.stock_svm_path, True)
        self.make_sure_path_exists()
    
    def backup_and_gen_predict(self):
        file_prefix = os.path.basename(os.path.splitext(self.stock_data_file)[0])

        file_prefix = file_prefix + "_" + "predict_"

        for path in os.listdir(self.stock_svm_path):
            if path.startswith(file_prefix) and not path.startswith(self.predict_file):
                shutil.move(os.path.join(self.stock_svm_path, path),
                            os.path.join(self.model_history_path, path))

    def _svm_model_gen(self):
        f = open(self.stock_data_file,'rb')

        h_10_5 = os.path.join(self.svm_tmp_path,
            '{0}_h_{1}_{2}_data'.format(self.model_file, self.look_back_days, self.predict_days))
        l_10_5 = os.path.join(self.svm_tmp_path,
            '{0}_l_{1}_{2}_data'.format(self.model_file, self.look_back_days, self.predict_days))
        m_h_10_5 = os.path.join(self.stock_svm_path,
            '{0}_h_{1}_{2}_model'.format(self.model_file, self.look_back_days, self.predict_days))
        m_l_10_5 = os.path.join(self.stock_svm_path,
            '{0}_l_{1}_{2}_model'.format(self.model_file, self.look_back_days, self.predict_days))
        r_h_10_5 = os.path.join(self.stock_svm_path,
            '{0}_h_{1}_{2}_range'.format(self.model_file, self.look_back_days, self.predict_days))
        r_l_10_5 = os.path.join(self.stock_svm_path,
            '{0}_l_{1}_{2}_range'.format(self.model_file, self.look_back_days, self.predict_days))

        f_m_data_h = open(h_10_5, 'w')
        f_m_data_l = open(l_10_5, 'w')

        f.seek(0, os.SEEK_SET)
        self.generator.generate_model_data(f,
                                      svm_generator.LBL_HIGH, svm_generator.LVL_9, f_m_data_h, self.forward_days)
        f.seek(0, os.SEEK_SET)
        self.generator.generate_model_data(f,
                                      svm_generator.LBL_LOW, svm_generator.LVL_9, f_m_data_l, self.forward_days)

        f.close()
        f_m_data_h.close()
        f_m_data_l.close()

        self.svm_tools.gen_model(h_10_5, m_h_10_5, r_h_10_5, self.svm_tmp_path)
        self.svm_tools.gen_model(l_10_5, m_l_10_5, r_l_10_5, self.svm_tmp_path)

    def get_predict_result_file_name(self, predict_file):
        return os.path.join(self.stock_svm_path,
                '{0}_p_{1}_{2}_predict'.format(predict_file, self.look_back_days, self.predict_days))

    def get_h_model_data_file_name(self):
        return os.path.join(self.svm_tmp_path,
            '{0}_h_{1}_{2}_data'.format(self.model_file, self.look_back_days, self.predict_days))

    def get_l_model_data_file_name(self):
        return os.path.join(self.svm_tmp_path,
            '{0}_l_{1}_{2}_data'.format(self.model_file, self.look_back_days, self.predict_days))
        
    def get_h_model_file_name(self):
        return os.path.join(self.stock_svm_path,
            '{0}_h_{1}_{2}_model'.format(self.model_file, self.look_back_days, self.predict_days))

    def get_l_model_file_name(self):
        return os.path.join(self.stock_svm_path,
            '{0}_l_{1}_{2}_model'.format(self.model_file, self.look_back_days, self.predict_days))

    def get_h_model_data_file_name_2(self, model_file):
        return os.path.join(self.svm_tmp_path,
            '{0}_h_{1}_{2}_data'.format(model_file, self.look_back_days, self.predict_days))

    def get_l_model_data_file_name_2(self, model_file):
        return os.path.join(self.svm_tmp_path,
            '{0}_l_{1}_{2}_data'.format(model_file, self.look_back_days, self.predict_days))
        
    def get_h_model_file_name_2(self, model_file):
        return os.path.join(self.stock_svm_path,
            '{0}_h_{1}_{2}_model'.format(model_file, self.look_back_days, self.predict_days))

    def get_l_model_file_name_2(self, model_file):
        return os.path.join(self.stock_svm_path,
            '{0}_l_{1}_{2}_model'.format(model_file, self.look_back_days, self.predict_days))

    def add_stock_data_to_model(self, stock_data_file):
        f = open(stock_data_file,'rb')

        h_10_5 = os.path.join(self.svm_tmp_path,
            '{0}_h_{1}_{2}_data'.format(self.model_file, self.look_back_days, self.predict_days))
        l_10_5 = os.path.join(self.svm_tmp_path,
            '{0}_l_{1}_{2}_data'.format(self.model_file, self.look_back_days, self.predict_days))

        f_m_data_h = open(h_10_5, 'a+')
        f_m_data_l = open(l_10_5, 'a+')

        f.seek(0, os.SEEK_SET)
        self.generator.generate_model_data(f,
                                      svm_generator.LBL_HIGH, svm_generator.LVL_9, f_m_data_h, self.forward_days)
        f.seek(0, os.SEEK_SET)
        self.generator.generate_model_data(f,
                                      svm_generator.LBL_LOW, svm_generator.LVL_9, f_m_data_l, self.forward_days)

        f_m_data_h.close()
        f_m_data_l.close()
        f.close()
        
    def add_stock_data_to_model_with_model_and_node_names(self, stock_data_file, model_files_and_nodes_names):
        class OutputCallback(object):
            def __init__(self, stock_svm, model_file, nodes_names):
                self.stock_svm = stock_svm
                self.model_file = model_file
                self.nodes_names = nodes_names
                h_10_5 = os.path.join(stock_svm.svm_tmp_path,
                    '{0}_h_{1}_{2}_data'.format(model_file, stock_svm.look_back_days, stock_svm.predict_days))
                l_10_5 = os.path.join(stock_svm.svm_tmp_path,
                    '{0}_l_{1}_{2}_data'.format(model_file, stock_svm.look_back_days, stock_svm.predict_days))

                self.f_m_data_h = open(h_10_5, 'a+')
                self.f_m_data_l = open(l_10_5, 'a+')

            def get_output_file(self, label_flags):
                if label_flags == svm_generator.LBL_HIGH:
                    return self.f_m_data_h
                elif label_flags == svm_generator.LBL_LOW:
                    return self.f_m_data_l
                else:
                    assert False, "invalid label_flag:{0}".format(label_flags)

            def should_output_name(self, name):
                if self.nodes_names is None:
                    return True

                return name in self.nodes_names
                    
            def close(self):
                self.f_m_data_h.close()
                self.f_m_data_l.close()
        #end class OutputCallback
                
        f = open(stock_data_file,'rb')

        output_callbacks = []
        for (model_file, nodes_names) in model_files_and_nodes_names:
            output_callback = OutputCallback(self, model_file, nodes_names)
            output_callbacks.append(output_callback)
            
        f.seek(0, os.SEEK_SET)
        self.generator.generate_model_data_with_callbacks(f,
                                      svm_generator.LBL_HIGH,
                                      svm_generator.LVL_9, self.forward_days,
                                      output_callbacks)
        f.seek(0, os.SEEK_SET)
        self.generator.generate_model_data_with_callbacks(f,
                                      svm_generator.LBL_LOW,
                                      svm_generator.LVL_9, self.forward_days,
                                      output_callbacks)

        f.close()
        
        for output_callback in output_callbacks:
            output_callback.close()

    def do_model_gen(self, lower_limit = -1):
        h_10_5 = os.path.join(self.svm_tmp_path,
            '{0}_h_{1}_{2}_data'.format(self.model_file, self.look_back_days, self.predict_days))
        l_10_5 = os.path.join(self.svm_tmp_path,
            '{0}_l_{1}_{2}_data'.format(self.model_file, self.look_back_days, self.predict_days))
        m_h_10_5 = os.path.join(self.stock_svm_path,
            '{0}_h_{1}_{2}_model'.format(self.model_file, self.look_back_days, self.predict_days))
        m_l_10_5 = os.path.join(self.stock_svm_path,
            '{0}_l_{1}_{2}_model'.format(self.model_file, self.look_back_days, self.predict_days))
        r_h_10_5 = os.path.join(self.stock_svm_path,
            '{0}_h_{1}_{2}_range'.format(self.model_file, self.look_back_days, self.predict_days))
        r_l_10_5 = os.path.join(self.stock_svm_path,
            '{0}_l_{1}_{2}_range'.format(self.model_file, self.look_back_days, self.predict_days))

        self.svm_tools.gen_model(h_10_5, m_h_10_5, r_h_10_5, self.svm_tmp_path, lower_limit)
        self.svm_tools.gen_model(l_10_5, m_l_10_5, r_l_10_5, self.svm_tmp_path, lower_limit)

    def do_predict(self, lower_limit = -1):
        self.do_predict_for_stock(self.stock_data_file, lower_limit)
        
    def do_predict_for_stock(self, stock_data_file, lower_limit = -1):
        f = open(stock_data_file,'rb')

        predict_file = self.gen_predict_file_name(stock_data_file)

        p_10_5_d = os.path.join(self.svm_tmp_path,
            '{0}_p_{1}_{2}_data'.format(predict_file, self.look_back_days, self.predict_days))
        p_10_5 = self.get_predict_result_file_name(predict_file)
        r_h_10_5 = os.path.join(self.stock_svm_path,
            '{0}_h_{1}_{2}_range'.format(self.model_file, self.look_back_days, self.predict_days))
        r_l_10_5 = os.path.join(self.stock_svm_path,
            '{0}_l_{1}_{2}_range'.format(self.model_file, self.look_back_days, self.predict_days))
        m_h_10_5 = os.path.join(self.stock_svm_path,
            '{0}_h_{1}_{2}_model'.format(self.model_file, self.look_back_days, self.predict_days))
        m_l_10_5 = os.path.join(self.stock_svm_path,
            '{0}_l_{1}_{2}_model'.format(self.model_file, self.look_back_days, self.predict_days))

        f_p_10_5_d = open(p_10_5_d, "w")
        
        self.generator.generate_predict_data(f, svm_generator.LVL_9, f_p_10_5_d)

        #read last date of stock data
        d = data.data_loader.read_next_day_data(f,
                                                -1,
                                                os.SEEK_END)

        f.close()
        f_p_10_5_d.close()

        f = open(p_10_5, "a+")

        print(strftime("%Y%m%d", localtime()), end=',', file = f)
        print(d.date, end=',', file = f)
        l_low = l = self.svm_tools.gen_predict(p_10_5_d, m_l_10_5, r_l_10_5, self.svm_tmp_path, lower_limit)
        #print(self.generator.label_to_level(l), end=',', file = f)
        print(l, end=',', file = f)
        l_high = l = self.svm_tools.gen_predict(p_10_5_d, m_h_10_5, r_h_10_5, self.svm_tmp_path, lower_limit)
        #print(self.generator.label_to_level(l), file = f)
        print(l, end=',', file = f)
        #close price and predict low/high price
        p_1, p_2 = self.generator.label_to_price(d.close_price, l_low)
        print(p_1, end=',', file = f)
        print(p_2, end=',', file = f)
        p_1, p_2 = self.generator.label_to_price(d.close_price, l_high)
        print(p_1, end=',', file = f)
        print(p_2, file = f)

        f.close()

    def reset_nodes(self):
        self.generator.build_nodes()
        
    def nodes_names(self):
        self.generator.build_nodes()
        return self.generator.nodes_names

    def nodes_manager(self):
        return self.generator.nm
