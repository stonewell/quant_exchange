# -*- coding: utf-8 -*-
import core.node
import basic_node
import price_node
from general_osc_node import GeneralOSCNode

############## EMA ###########################
class EMANode(core.node.Node):
    def __init__(self, nm, from_name, days = 6):
        core.node.Node.__init__(self, nm, "%s_EMA_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        nm.register_output_wire(from_name, self)

    def consume(self, from_name, value):
        if self.from_name != from_name:
            return None

## 1、计算移动平均值（EMA）
## 12日EMA的算式为
## EMA（12）=前一日EMA（12）×11/13＋今日收盘价×2/13
## 26日EMA的算式为
## EMA（26）=前一日EMA（26）×25/27＋今日收盘价×2/27
## 2、计算离差值（DIF）
## DIF=今日EMA（12）－今日EMA（26）
        v = 2 * value / (self.days + 1)

        if len(self.values) > 0:
            v += ((self.days - 1) * self.values[len(self.values) - 1] / (self.days + 1))

        return v

################# DIF ########################
class DIFNode(core.node.Node):
    def __init__(self, nm, from_name, days1 = 12, days2 = 26):
        core.node.Node.__init__(self, nm, "%s_DIF_%d_%d" % (from_name, days1, days2))

        self.from_name = from_name
        self.days1 = days1
        self.days2 = days2

        self.ema_name1 = "%s_EMA_%d" % (from_name, days1)
        self.ema_name2 = "%s_EMA_%d" % (from_name, days2)

        nm.register_output_wire(self.ema_name1, self)
        nm.register_output_wire(self.ema_name2, self)

        self.clear_saved_value()

    def clear_saved_value(self):
        self.ema_v1 = None
        self.ema_v2 = None

    def consume(self, from_name, value):
        if self.ema_name1 == from_name:
            self.ema_v1 = value

        if self.ema_name2 == from_name:
            self.ema_v2 = value

        v = None

        if (self.ema_v1 != None and
            self.ema_v2 != None):
            v = self.ema_v1 - self.ema_v2
            self.clear_saved_value()

        return v

################# DEA ########################
class DEANode(core.node.Node):
    def __init__(self, nm, from_name, days1 = 12, days2 = 26, days3 = 3):
        core.node.Node.__init__(self, nm, "%s_DEA_%d_%d_%d" % (from_name, days1, days2, days3))

        self.from_name = from_name
        self.days1 = days1
        self.days2 = days2
        self.days3 = days3

        self.dif_name = "%s_DIF_%d_%d" % (from_name, days1, days2)

        nm.register_output_wire(self.dif_name, self)

    def consume(self, from_name, value):
        if self.dif_name != from_name:
            return None

        v = 2 * value / (self.days3 + 1)

        if len(self.values) > 0:
            v += ((self.days3 - 1) 
                  * self.values[len(self.values) - 1] 
                  / (self.days3 + 1))

        return v

################# MACD ########################
class MACDNode(core.node.Node):
    def __init__(self, nm, from_name, days1 = 12, days2 = 26, days3 = 9):
        core.node.Node.__init__(self, nm, "%s_MACD_%d_%d_%d" % (from_name, days1, days2, days3))

        self.from_name = from_name
        self.days1 = days1
        self.days2 = days2
        self.days3 = days3

        self.dif_name = "%s_DIF_%d_%d" % (from_name, days1, days2)
        self.dea_name = "%s_DEA_%d_%d_%d" % (from_name, days1, days2, days3)

        nm.register_output_wire(self.dif_name, self)
        nm.register_output_wire(self.dea_name, self)

        self.clear_saved_value()

    def clear_saved_value(self):
        self.dif_v = None
        self.dea_v = None

    def consume(self, from_name, value):
        if self.dif_name != from_name and self.dea_name != from_name:
            return None

        if self.dif_name == from_name:
            self.dif_v = value

        if self.dea_name == from_name:
            self.dea_v = value

        v = None
        
        if self.dea_v is not None and self.dif_v is not None:
            v = self.dif_v - self.dea_v

            self.clear_saved_value()

        return v

class MACDOSCNode(GeneralOSCNode):
    def __init__(self, nm, from_name, days1 = 12, days2 = 26, days3 = 9):
        GeneralOSCNode.__init__(self, nm,
                                "%s_MACD_OSC_%d_%d_%d" % (from_name, days1, days2, days3),
                                "%s_DIF_%d_%d" % (from_name, days1, days2),
                                "%s_DEA_%d_%d_%d" % (from_name, days1, days2, days3))

################# Helper functions ###############
def create_ema_node(nm, from_name, days = 6, capacity = 15):
    _name = "%s_EMA_%d" % (from_name, days)

    if not _name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        n = EMANode(nm, from_name, days)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]

def create_dif_node(nm, from_name, days1 = 12, days2 = 26, capacity = 15):
    _name = "%s_DIF_%d_%d" % (from_name, days1, days2)

    if not _name in nm.nodes:
        create_ema_node(nm, from_name, days1, capacity)
        create_ema_node(nm, from_name, days2, capacity)

        n = DIFNode(nm, from_name, days1, days2)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]

def create_dea_node(nm, from_name, days1 = 12, days2 = 26, days3 = 9, capacity = 15):
    _name = "%s_DEA_%d_%d_%d" % (from_name, days1, days2, days3)

    if not _name in nm.nodes:
        create_dif_node(nm, from_name, days1, days2, capacity)

        n = DEANode(nm, from_name, days1, days2, days3)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]

def create_macd_node(nm, from_name, days1 = 12, days2 = 26, days3 = 9, capacity = 15):
    _name = "%s_MACD_%d_%d_%d" % (from_name, days1, days2, days3)

    if not _name in nm.nodes:
        create_dea_node(nm, from_name, days1, days2, days3, capacity)

        n = MACDNode(nm, from_name, days1, days2, days3)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]

def create_macd_osc_node(nm, from_name, days1 = 12, days2 = 26, days3 = 9, capacity = 15):
    _name = "%s_MACD_OSC_%d_%d_%d" % (from_name, days1, days2, days3)

    if not _name in nm.nodes:
        create_macd_node(nm, from_name, days1, days2, days3, capacity)

        n = MACDOSCNode(nm, from_name, days1, days2, days3)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]
