import collections

import core.nodes_manager
import core.nodes.kdj_node
import core.nodes.macd_node
import core.nodes.k_line_node
import core.nodes.osc_node
import core.nodes.basic_node

def create_nodes_k_line(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.k_line_node.create_k_line_node(nm, capacity).name)

    return node_names
    
def create_nodes_r_5(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 5, capacity).name)

    return node_names
    
def create_nodes_r_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 11, capacity).name)

    return node_names

def create_nodes_r_19(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 19, capacity).name)

    return node_names

def create_nodes_r_osc_5_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_r_osc_node(nm, from_name, 5, 11, capacity).name)

    return node_names
    
def create_nodes_r_osc_func(day1, day2):
    def internal_create_nodes_r_osc_func(nm, from_name, capacity):
        node_names = []
        node_names.append(core.nodes.basic_node.create_r_osc_node(nm, from_name, day1, day2, capacity).name)

        return node_names

    return internal_create_nodes_r_osc_func

def create_nodes_rsi_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 11, capacity).name)

    return node_names

def create_nodes_rsi_5(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 5, capacity).name)

    return node_names

def create_nodes_rsi_19(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 19, capacity).name)

    return node_names

def create_nodes_rsi_osc_func(day1, day2):
    def internal_create_nodes_rsi_osc(nm, from_name, capacity):
        node_names = []
        node_names.append(core.nodes.basic_node.create_rsi_osc_node(nm, from_name, day1, day2, capacity).name)

        return node_names

    return internal_create_nodes_rsi_osc

def create_nodes_rsi_osc_5_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_rsi_osc_node(nm, from_name, 5, 11, capacity).name)

    return node_names

def create_nodes_dif_12_26(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.macd_node.create_dif_node(nm, from_name, 12, 26, capacity).name)

    return node_names
    
def create_nodes_dea_12_26_3(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.macd_node.create_dea_node(nm, from_name, 12, 26, 3, capacity).name)

    return node_names
    
def create_nodes_dea_12_26_9(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.macd_node.create_dea_node(nm, from_name, 12, 26, 9, capacity).name)

    return node_names
    
def create_nodes_macd_12_26_9(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.macd_node.create_macd_node(nm, from_name, 12, 26, 9, capacity).name)

    return node_names

def create_nodes_macd_osc_12_26_9(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.macd_node.create_macd_osc_node(nm, from_name, 12, 26, 9, capacity).name)

    return node_names

def create_nodes_rsv_5(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_rsv_node(nm, from_name, 5, capacity).name)

    return node_names

def create_nodes_rsv_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_rsv_node(nm, from_name, 11, capacity).name)

    return node_names

def create_nodes_kd_19(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_kd_node(nm, from_name, 19, capacity).name)

    return node_names

def create_nodes_kd_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_kd_node(nm, from_name, 11, capacity).name)

    return node_names

def create_nodes_kd_5(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_kd_node(nm, from_name, 5, capacity).name)

    return node_names

def create_nodes_k_5(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_k_node(nm, from_name, 5, capacity).name)

    return node_names

def create_nodes_k_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_k_node(nm, from_name, 11, capacity).name)

    return node_names

def create_nodes_d_5(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_d_node(nm, from_name, 5, capacity).name)

    return node_names

def create_nodes_d_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_d_node(nm, from_name, 11, capacity).name)

    return node_names

def create_nodes_j_5(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_j_node(nm, from_name, 5, capacity).name)

    return node_names

def create_nodes_j_11(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.kdj_node.create_j_node(nm, from_name, 11, capacity).name)

    return node_names
    
def create_nodes_ma_5(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_ma_node(nm, from_name, 5, capacity).name)

    return node_names

def create_nodes_ma_10(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_ma_node(nm, from_name, 10, capacity).name)

    return node_names

def create_nodes_osc_func(nm, from_name, capacity, day1, day2):
    def internal_create_nodes_osc(nm, from_name, capacity):
        node_names = []
        node_names.append(core.nodes.osc_node.create_osc_node(nm, from_name, day1, day2, capacity).name)

        return node_names
        
    return internal_create_nodes_osc

def create_nodes_osc_5_10(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.osc_node.create_osc_node(nm, from_name, 5, 10, capacity).name)

    return node_names

def create_nodes_osc_10_20(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.osc_node.create_osc_node(nm, from_name, 10, 20, capacity).name)

    return node_names

def create_nodes_human(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 11, capacity).name)

    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 11, capacity).name)

    node_names.append(core.nodes.macd_node.create_dif_node(nm, from_name, 12, 26, capacity).name)
    node_names.append(core.nodes.macd_node.create_dea_node(nm, from_name, 12, 26, 9, capacity).name)

    node_names.append(core.nodes.kdj_node.create_rsv_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.kdj_node.create_rsv_node(nm, from_name, 11, capacity).name)

    node_names.append(core.nodes.basic_node.create_ma_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.basic_node.create_ma_node(nm, from_name, 10, capacity).name)

    if not (from_name == 'Amount'):
        node_names.append(core.nodes.k_line_node.create_k_line_node(nm, capacity).name)
    return node_names

def create_nodes_ensemble(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 11, capacity).name)

    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 11, capacity).name)

    node_names.append(core.nodes.macd_node.create_dif_node(nm, from_name, 12, 26, capacity).name)
    node_names.append(core.nodes.macd_node.create_dea_node(nm, from_name, 12, 26, 9, capacity).name)

    node_names.append(core.nodes.kdj_node.create_rsv_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.kdj_node.create_rsv_node(nm, from_name, 11, capacity).name)

    node_names.append(core.nodes.basic_node.create_ma_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.basic_node.create_ma_node(nm, from_name, 10, capacity).name)

    if not (from_name == 'Amount'):
        node_names.append(core.nodes.k_line_node.create_k_line_node(nm, capacity).name)
    return node_names

def create_nodes_6(nm, from_name, capacity):
    node_names = []
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.basic_node.create_r_node(nm, from_name, 11, capacity).name)

    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.basic_node.create_rsi_node(nm, from_name, 11, capacity).name)

    node_names.append(core.nodes.macd_node.create_dif_node(nm, from_name, 12, 26, capacity).name)
    node_names.append(core.nodes.macd_node.create_dea_node(nm, from_name, 12, 26, 3, capacity).name)

    node_names.append(core.nodes.kdj_node.create_rsv_node(nm, from_name, 5, capacity).name)
    node_names.append(core.nodes.kdj_node.create_rsv_node(nm, from_name, 11, capacity).name)

    return node_names
    
def create_nodes_1(nm, from_name, capacity):
    core.nodes.basic_node.create_ma_node(nm, from_name, 11, capacity)
    core.nodes.basic_node.create_ma_node(nm, from_name, 5, capacity)

    core.nodes.basic_node.create_r_node(nm, from_name, 5, capacity)
    core.nodes.basic_node.create_rsi_node(nm, from_name, 5, capacity)

    core.nodes.macd_node.create_dif_node(nm, from_name, 12, 26, capacity)
    core.nodes.macd_node.create_dea_node(nm, from_name, 12, 26, 3, capacity)

    core.nodes.kdj_node.create_rsv_node(nm, from_name, 5, capacity)

def create_nodes_2(nm, from_name, capacity):
    core.nodes.basic_node.create_ma_node(nm, from_name, 11, capacity)
    core.nodes.basic_node.create_ma_node(nm, from_name, 5, capacity)

def create_nodes_3(nm, from_name, capacity):
    core.nodes.macd_node.create_dif_node(nm, from_name, 12, 26, capacity)
    core.nodes.macd_node.create_dea_node(nm, from_name, 12, 26, 3, capacity)

def create_nodes_4(nm, from_name, capacity):
    core.nodes.basic_node.create_ma_node(nm, from_name, 11, capacity)
    core.nodes.basic_node.create_ma_node(nm, from_name, 5, capacity)

    core.nodes.macd_node.create_dif_node(nm, from_name, 12, 26, capacity)
    core.nodes.macd_node.create_dea_node(nm, from_name, 12, 26, 3, capacity)

def create_nodes_5(nm, from_name, capacity):
    core.nodes.basic_node.create_r_node(nm, from_name, 5, capacity)
    core.nodes.basic_node.create_r_node(nm, from_name, 11, capacity)

    core.nodes.basic_node.create_rsi_node(nm, from_name, 5, capacity)
    core.nodes.basic_node.create_rsi_node(nm, from_name, 11, capacity)

    core.nodes.kdj_node.create_rsv_node(nm, from_name, 5, capacity)
    core.nodes.kdj_node.create_rsv_node(nm, from_name, 11, capacity)

FeatureSpec = collections.namedtuple('FeatureSpec', ['name', 'nodes_creator', 'full_file_generate_predict'])

def create_nodes_with_specs(nm, from_name, capacity, all_specs):
    nodes_names = []

    specs = all_specs

    if callable(specs):
        specs = specs()

    for (name, nc, f) in specs:
        nodes_names.extend(nc(nm, from_name, capacity))
    #end for

    return nodes_names
#end def
