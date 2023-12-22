import core.node
import price_node
import math
from general_osc_node import GeneralOSCNode

class ROSCNode(GeneralOSCNode):
    def __init__(self, nm, from_name, days1 = 5, days2 = 11):
        GeneralOSCNode.__init__(self, nm,
                                "%s_R_OSC_%d_%d" % (from_name, days1, days2),
                                "%s_R_%d" % (from_name, days1),
                                "%s_R_%d" % (from_name, days2),
                                delta_only = True)

class RSIOSCNode(GeneralOSCNode):
    def __init__(self, nm, from_name, days1 = 5, days2 = 11):
        GeneralOSCNode.__init__(self, nm,
                                "%s_RSI_OSC_%d_%d" % (from_name, days1, days2),
                                "%s_RSI_%d" % (from_name, days1),
                                "%s_RSI_%d" % (from_name, days2),
                                delta_only = True)

########### Extreme nodes (lowest higest) for days ###############
class ExtremeNode(core.node.Node):
    def __init__(self, nm, from_name, days = 10):
        core.node.Node.__init__(self, nm, "%s_Extreme_%d" % (from_name, days), days)

        self.from_name = from_name

        nm.register_output_wire(from_name, self)

    def data_income(self, from_name, value):
        self.values.append(value)

        while len(self.values) > self.capacity:
            del self.values[0]

        self.data_output("%s_Lowest_%d" % (self.from_name, self.capacity), min(self.values))
        self.data_output("%s_Highest_%d" % (self.from_name, self.capacity), max(self.values))

############ MA nodes ###################
class MANode(core.node.Node):
    def __init__(self, nm, from_name, days):
        core.node.Node.__init__(self, nm, "%s_MA_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.history_values = []

        nm.register_output_wire(from_name, self)

    def consume(self, from_name, value):
        if self.from_name != from_name:
            return None

        self.history_values.append(value)

        while len(self.history_values) > self.days:
            del self.history_values[0]

        v = math.fsum(self.history_values) / len(self.history_values)

        return v
########### R Node ##########################
class RNode(core.node.Node):
    def __init__(self, nm, from_name, days):
        core.node.Node.__init__(self, nm, "%s_R_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.highest_name = "%s_Highest_%d" % (from_name, days)
        self.lowest_name = "%s_Lowest_%d" % (from_name, days)

        nm.register_output_wire(self.highest_name, self)
        nm.register_output_wire(self.lowest_name, self)
        nm.register_output_wire(self.from_name, self)

        self.clear_saved_value()

    def clear_saved_value(self):
        self.saved_highest = None
        self.saved_lowest = None
        self.saved_from = None

    def consume(self, from_name, value):
        if from_name == self.from_name:
            self.saved_from = value

        if from_name == self.highest_name:
            self.saved_highest = value

        if from_name == self.lowest_name:
            self.saved_lowest = value

        v = None

        if self.saved_highest == self.saved_lowest:
            return None

        if (self.saved_from != None and
            self.saved_highest != None and
            self.saved_lowest != None):
            v = (100
                 * (self.saved_highest - self.saved_from)
                 / (self.saved_highest - self.saved_lowest))
            self.clear_saved_value()

        return v
################## RSI Node #####################
class RSINode(core.node.Node):
    def __init__(self, nm, from_name, days):
        core.node.Node.__init__(self, nm, "%s_RSI_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.history_values = []

        nm.register_output_wire(from_name, self)

    def consume(self, from_name, value):
        if self.from_name != from_name:
            return None

        self.history_values.append(value)

        while len(self.history_values) > self.days:
            del self.history_values[0]

        if len(self.history_values) == 0:
            return None

        A = 0.0
        B = 0.0
        last = self.history_values[0]

        for i in range(1, len(self.history_values)):
            delta = self.history_values[i] - last

            if (delta > 0):
                A += delta
            else:
                B += delta

            last = self.history_values[i]

        if A == 0.0 and B == 0.0:
            return None

        v = A * 100 / (A + B * -1)

        return v

################## Helper functions to create basic node ######################
def create_extreme_node(nm, from_name, days = 10, capacity = 15):
    extreme_name = "%s_Extreme_%d" % (from_name, days)

    if not extreme_name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        extreme = ExtremeNode(nm, from_name, days)
        nm.nodes[extreme_name] = extreme

        return extreme
    else:
        return nm.nodes[extreme_name]

def create_ma_node(nm, from_name, days, capacity = 15):
    ma_name = "%s_MA_%d" % (from_name, days)

    if not ma_name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        ma = MANode(nm, from_name, days)
        ma.capacity = capacity

        nm.nodes[ma_name] = ma

        return ma

    else:
        return nm.nodes[ma_name]

def create_r_node(nm, from_name, days, capacity = 15):
    r_name = "%s_R_%d" % (from_name, days)

    if not r_name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        create_extreme_node(nm, from_name, days, capacity)

        r = RNode(nm, from_name, days)
        r.capacity = capacity

        nm.nodes[r_name] = r

        return r
    else:
        return nm.nodes[r_name]

def create_rsi_node(nm, from_name, days, capacity = 15):
    rsi_name = "%s_RSI_%d" % (from_name, days)

    if not rsi_name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        rsi = RSINode(nm, from_name, days)
        rsi.capacity = capacity

        nm.nodes[rsi_name] = rsi

        return rsi

    else:
        return nm.nodes[rsi_name]

def create_rsi_osc_node(nm, from_name, days1=5, days2=11, capacity = 15):
    name = "%s_RSI_OSC_%d_%d" % (from_name, days1, days2)

    if not name in nm.nodes:
        create_rsi_node(nm, from_name, days1, capacity)
        create_rsi_node(nm, from_name, days2, capacity)

        n = RSIOSCNode(nm, from_name, days1, days2)
        n.capacity = capacity

        nm.nodes[name] = n

        return n

    else:
        return nm.nodes[name]

def create_r_osc_node(nm, from_name, days1=5, days2=11, capacity = 15):
    name = "%s_R_OSC_%d_%d" % (from_name, days1, days2)

    if not name in nm.nodes:
        create_r_node(nm, from_name, days1, capacity)
        create_r_node(nm, from_name, days2, capacity)

        n = ROSCNode(nm, from_name, days1, days2)
        n.capacity = capacity

        nm.nodes[name] = n

        return n

    else:
        return nm.nodes[name]
