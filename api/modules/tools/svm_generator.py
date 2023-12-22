from __future__ import print_function

import sys
import os
import math

import data.data_loader
import core.nodes_manager
import core.nodes.kdj_node
import core.nodes.macd_node
import stutils.util_funcs
import tools.svm_debug

LBL_HIGH = 4
LBL_LOW = 2
LBL_END = 1

LVL_2 = 0
LVL_9 = 1

name_outputed = False

class SVMGenerator(object):
    def __init__(self, nodes_creator, look_back_days, predict_days,
                 use_amount = True,
                 filter_zero = False,
                 output_day = True,
                 nodes_names = None):
        self.look_back_days = look_back_days  
        self.predict_days = predict_days
        self.capacity = look_back_days + predict_days
        self.nodes_creator = nodes_creator
        self.use_amount = use_amount
        self.filter_zero = filter_zero
        self.nodes_names = []
        self.prefer_nodes_names = nodes_names
        self.output_day = output_day

    def build_nodes(self):
        self.nm = nm = core.nodes_manager.NodesManager()

        #"PriceNode"
        core.nodes.price_node.create_price_node(nm, self.capacity)

        self.nodes_names = self.nodes_creator(nm, "Close", self.capacity)

        if (self.use_amount):
            amount_nodes_names = self.nodes_creator(nm, "Amount", self.capacity)
            if self.nodes_names is None:
                self.nodes_names = amount_nodes_names
            elif amount_nodes_names is not None:
                self.nodes_names.extend(amount_nodes_names)
        #end if use_amount

        #filter out nodes not prefered
        if self.prefer_nodes_names is not None:
            self.nodes_names = filter(lambda x:x in self.prefer_nodes_names, self.nodes_names)

        self.nodes_names = list(set(self.nodes_names))
    #end def build_nodes
        
    def generate_model_data(self, f, label_flags = LBL_HIGH, level_flags = LVL_9,
                            out_f = sys.stdout, forward_days = 3):
        class OutputCallback(object):
            def __init__(self, output_file, svm_generator):
                self.generator = svm_generator
                self.output_file = output_file

            def get_output_file(self, label_flags):
                return out_f

            def should_output_name(self, name):
                if self.generator.nodes_names is None:
                    return True

                return name in self.generator.nodes_names
        #end class OutputCallback

        self.generate_model_data_with_callbacks(f,
                                                 label_flags, level_flags,
                                                 forward_days,
                                                 [OutputCallback(out_f, self)])
    #generate_model_data
                    
    def generate_model_data_with_callbacks(self, f, label_flags, level_flags, forward_days, output_callbacks):
        self.build_nodes()
        
        nodes = []

        if "" in self.nm.output_wires:
            nodes = self.nm.output_wires[""]

        if nodes:
            done = False

            # Read data and create output values
            done = self.read_data(f, nodes, self.capacity)
                
            if done:
                for output_callback in output_callbacks:
                    self.output_line_with_callback(label_flags, level_flags,
                                                   gen_label = True,
                                                   output_callback = output_callback)
                
            while(not done):
                # generate a line out put
                for output_callback in output_callbacks:
                    self.output_line_with_callback(label_flags, level_flags,
                                                   gen_label = True,
                                                   output_callback = output_callback)

                # Read data and create output values
                tmp_forward_days = self.calculate_forward_days(forward_days, label_flags, level_flags)
                
                done = self.read_data(f, nodes, tmp_forward_days)

                if done:
                    for output_callback in output_callbacks:
                        self.output_line_with_callback(label_flags, level_flags,
                                                   gen_label = True,
                                                   output_callback = output_callback)
            #while(not done)
        #if nodes
    #end generate_model_data_with_callbacks

    def read_data(self, f, nodes, count):
        for i in range(count):
            d = data.data_loader.read_next_day_data(f)

            if (d == None):
                return True

            for node in nodes:
                node.data_income("", d)
        #for i in range(1, count)

        return False
        
    def output_line(self, f, label_flags, level_flags, gen_label = True):
        class OutputCallback(object):
            def __init__(self, output_file, svm_generator):
                self.generator = svm_generator
                self.output_file = output_file

            def get_output_file(self, label_flags):
                return f

            def should_output_name(self, name):
                if self.generator.nodes_names is None:
                    return True

                return name in self.generator.nodes_names
        #end class OutputCallback

        self.output_line_with_callback(label_flags, level_flags, gen_label,
                                       OutputCallback(f, self));
    #end output_line

    def output_line_with_callback(self,
                                  label_flags, level_flags,
                                  gen_label, output_callback, gen_predict_data = False):
        global name_outputed
        label = 0

        if gen_label:
            label = self.generate_label(label_flags,
                                        level_flags)

        index = 1
        output_file = output_callback.get_output_file(label_flags)

        print(label, end=' ', file = output_file)

        if not name_outputed:
            print("----------------node names:", sorted(self.nm.nodes.keys()))
            name_outputed = True

        for name in sorted(self.nm.nodes.keys()):
            if (name != 'Price') and \
                (output_callback.should_output_name(name)):
                if gen_predict_data:
                    values = self.nm.nodes[name].snapshot()
                    values = values[len(values) - self.look_back_days:]
                else:
                    values = self.nm.nodes[name].snapshot()[0:self.look_back_days]
                    
                if tools.svm_debug.debug_svm:
                    print("++++++",len(values), name, values)
                for v in values:
                    if not self.filter_zero or v != 0:
                        if self.output_day:
                            print(index, ':', sep='', end='', file=output_file)
                        print(v, sep='', end=' ', file=output_file)
                        
                    index = index + 1
                #for v in values
        #for name in nm.nodes
                    
        print('', file = output_file)
    #end output_line_with_callback
        
    def generate_label(self, flags, level_flags):
        price_values = self.nm.nodes['Price'].snapshot()
        close_values = [v.close_price for v in price_values][self.look_back_days:]

        if len(close_values) == 0:
            return 0

        start_value = close_values[0]

        if len(close_values) == 1:
            start_value = price_values[self.look_back_days - 1].close_price
            
        end_value = close_values[len(close_values) - 1]
        high_value = max(close_values)
        low_value = min(close_values)

        if (start_value == 0):
            return 0

        label = 0
        
        if flags == LBL_HIGH:
            label = self.level((high_value - start_value) * 100 / start_value, level_flags)

        if flags == LBL_LOW:
            label = self.level((low_value - start_value) * 100 / start_value, level_flags)

        if flags == LBL_END:
            label = self.level((end_value - start_value) * 100 / start_value, level_flags)

        assert label != 0, ("Invalid Label flags:%d can only be %d, %d or %d" %
                            (flags, LBL_HIGH, LBL_LOW, LBL_END))
        
        return label

    def level(self, v, flags):
        if flags == LVL_2:
            if v <= 0:
                return 1
            else:
                return 2
        #if flags == LVL_2

        if flags == LVL_9:
            if v < -8:
                return 1
            elif v < -5:
                return 2
            elif v < -2:
                return 3
            elif v < 0:
                return 4
            elif v == 0:
                return 5
            elif v < 2:
                return 6
            elif v < 5:
                return 7
            elif v < 8:
                return 8
            else:
                return 9
        #if flags == LVL_9

        assert False, "Invalid level flags:%d can only be %d or %d" % (flags, LVL_2, LVL_9)

    def label_to_level(self, v):
        if v == 0:
            return "unkown"
            
        if v == 1:
            return "<-8"
        elif v == 2:
            return "-8 < -5"
        elif v == 3:
            return "-5 < -2"
        elif v == 4:
            return "-2<0"
        elif v == 5:
            return "0"
        elif v == 6:
            return "0<2"
        elif v == 7:
            return "2<5"
        elif v == 8:
            return "5<8"
        else:
            return ">8"

    def label_to_price(self, base_price, v):
        if v == 0:
            return ("unkown", "unknown")
            
        if v == 1:
            return (base_price * (1 - 0.10), base_price * (1 - 0.08))
        elif v == 2:
            return (base_price * (1 - 0.08), base_price * (1 - 0.05))
        elif v == 3:
            return (base_price * (1 - 0.05), base_price * (1 - 0.02))
        elif v == 4:
            return (base_price * (1 - 0.02), base_price * (1 - 0.0))
        elif v == 5:
            return (base_price * (1 - 0.0), base_price * (1 - 0.0))
        elif v == 6:
            return (base_price * (1 - 0.0), base_price * (1 + 0.02))
        elif v == 7:
            return (base_price * (1 + 0.02), base_price * (1 + 0.05))
        elif v == 8:
            return (base_price * (1 + 0.05), base_price * (1 + 0.08))
        else:
            return (base_price * (1 + 0.08), base_price * (1 + 0.10))

    def generate_predict_data(self, f, level_flags = LVL_9, out_f = sys.stdout):
        class OutputCallback(object):
            def __init__(self, svm_generator):
                self.generator = svm_generator

            def get_output_file(self, label_flags):
                return out_f

            def should_output_name(self, name):
                if self.generator.nodes_names is None:
                    return True

                return name in self.generator.nodes_names
        #end class OutputCallback
        self.generate_predict_data_with_callback(f, level_flags, OutputCallback(self))
    
    def generate_predict_data_with_callback(self, f, output_callback, level_flags = LVL_9):
        self.build_nodes()
        
        nodes = []

        if "" in self.nm.output_wires:
            nodes = self.nm.output_wires[""]

        if nodes:
            # Read data and create output values
            # Read 10 times of capacity to make sure all formula get the right value
            count = self.capacity * 10
            last_d = None
            
            for i in range(0, count):
                d = data.data_loader.read_next_day_data(f,
                                                        -1 * (count - i),
                                                        os.SEEK_END)

                if (d == None):
                    break

                for node in nodes:
                    node.data_income("", d)

                last_d = d
            #for i in range(1, count)
                
            self.output_line_with_callback(LBL_HIGH, level_flags,
                                           False,
                                           output_callback,
                                           True) #generate predict data
    #end def generate_predict_data_with_callback

    def generate_predict_data_with_callback_2(self, f, output_callback, level_flags = LVL_9):
        self.build_nodes()
        
        nodes = []

        if "" in self.nm.output_wires:
            nodes = self.nm.output_wires[""]

        if nodes:
            last_d = None

            #always read all stock data
            f.seek(0, os.SEEK_SET)
            
            while True:
                d = data.data_loader.read_next_day_data(f)

                if (d == None):
                    break

                for node in nodes:
                    node.data_income("", d)

                last_d = d
            #end while
                
            self.output_line_with_callback(LBL_HIGH, level_flags,
                                           False,
                                           output_callback,
                                           True) #generate predict data
    #end def generate_predict_data_with_callback_2

    def generate_validate_data_with_callback(self, f, output_callback, level_flags = LVL_9):
        self.build_nodes()
        
        nodes = []

        if "" in self.nm.output_wires:
            nodes = self.nm.output_wires[""]

        if nodes:
            # Read data and create output values
            # Read 10 times of capacity to make sure all formula get the right value
            count = self.capacity * 10
            last_d = None
            
            for i in range(0, count):
                d = data.data_loader.read_next_day_data(f,
                                                        -1 * (count - i),
                                                        os.SEEK_END)

                if (d == None):
                    break

                for node in nodes:
                    node.data_income("", d)

                last_d = d
            #for i in range(1, count)
                
            self.output_line_with_callback(LBL_HIGH, level_flags,
                                           True, #gen_label
                                           output_callback,
                                           False) #not generate predict data
    #end def generate_validate_data_with_callback

    def generate_validate_data_with_callback_2(self, f, output_callback, level_flags = LVL_9):
        self.build_nodes()
        
        nodes = []

        if "" in self.nm.output_wires:
            nodes = self.nm.output_wires[""]

        if nodes:
            last_d = None
            
            #always read all stock data
            f.seek(0, os.SEEK_SET)

            while True:
                d = data.data_loader.read_next_day_data(f)

                if (d == None):
                    break

                for node in nodes:
                    node.data_income("", d)

                last_d = d
            #end while
                
            self.output_line_with_callback(LBL_HIGH, level_flags,
                                           True, #gen_label
                                           output_callback,
                                           False) #not generate predict data
    #end def generate_validate_data_with_callback_2

    def calculate_forward_days(self, default_forward_days, flags, level_flags):
        price_values = self.nm.nodes['Price'].snapshot()
        close_values = [v.close_price for v in price_values][self.look_back_days:]

        if len(close_values) == 0:
            return default_forward_days

        if flags == LBL_END:
            return default_forward_days

        high_value = max(close_values)
        low_value = min(close_values)

        for i in range(len(close_values)):
            if flags == LBL_HIGH:
                if close_values[i] == high_value:
                    return i + 1
            elif flags == LBL_LOW:
                if close_values[i] == low_value:
                    return i + 1
        #end for

        return default_forward_days
    #end def calculate_forward_days
