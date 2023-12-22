import core.node
import basic_node
import price_node
from general_osc_node import GeneralOSCNode

class KDNode(GeneralOSCNode):
    def __init__(self, nm, from_name, days1 = 6):
        GeneralOSCNode.__init__(self, nm,
                                "%s_KD_%d" % (from_name, days1),
                                "%s_K_%d" % (from_name, days1),
                                "%s_D_%d" % (from_name, days1),
                                delta_only = True,
                                norm_func = int)

############## RSV ###########################
class RSVNode(core.node.Node):
    def __init__(self, nm, from_name, days = 6):
        core.node.Node.__init__(self, nm, "%s_RSV_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.lowest_name = "%s_Lowest_%d" % (self.from_name, self.days)
        self.highest_name = "%s_Highest_%d" % (self.from_name, self.days)

        nm.register_output_wire(self.lowest_name, self)
        nm.register_output_wire(self.highest_name, self)
        nm.register_output_wire(from_name, self)

        self.clear_saved_value()

    def clear_saved_value(self):
        self.saved_lowest = None
        self.saved_highest = None
        self.saved_base_value = None

    def consume(self, from_name, value):
        if from_name == self.lowest_name:
            self.saved_lowest = value

        if from_name == self.highest_name:
            self.saved_highest = value

        if self.from_name == from_name:
            self.saved_base_value = value

        rsv = None

        if (self.saved_lowest != None and 
            self.saved_highest != None and
            self.saved_base_value != None):

            if self.saved_highest == self.saved_lowest:
                rsv = 0
            else:
                rsv = (100 
                       * (self.saved_base_value - self.saved_lowest)
                       / (self.saved_highest - self.saved_lowest))

            # clear saved value
            self.clear_saved_value()

        return rsv

############### K ####################
class KNode(core.node.Node):
    def __init__(self, nm, from_name, days = 6):
        core.node.Node.__init__(self, nm, "%s_K_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.rsv_name = "%s_RSV_%d" % (self.from_name, self.days)

        nm.register_output_wire(self.rsv_name, self)

    def consume(self, from_name, value):
        if from_name != self.rsv_name:
            return None

        last_k = 50

        if len(self.values) > 0:
            last_k = self.values[len(self.values) - 1]

        k = last_k * 2 / 3 + value / 3

        return k

############### D ####################
class DNode(core.node.Node):
    def __init__(self, nm, from_name, days = 6):
        core.node.Node.__init__(self, nm, "%s_D_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.k_name = "%s_K_%d" % (self.from_name, self.days)

        nm.register_output_wire(self.k_name, self)

    def consume(self, from_name, value):
        if from_name != self.k_name:
            return None

        last_d = 50

        if len(self.values) > 0:
            last_d = self.values[len(self.values) - 1]

        d = last_d * 2 / 3 + value / 3

        return d

############## J #####################
class JNode(core.node.Node):
    def __init__(self, nm, from_name, days = 6):
        core.node.Node.__init__(self, nm, "%s_J_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.k_name = "%s_K_%d" % (self.from_name, self.days)
        self.d_name = "%s_D_%d" % (self.from_name, self.days)

        nm.register_output_wire(self.k_name, self)
        nm.register_output_wire(self.d_name, self)

        self.clear_saved_value()

    def clear_saved_value(self):
        self.saved_d = None
        self.saved_k = None

    def consume(self, from_name, value):
        if (from_name == self.k_name):
            self.saved_k = value

        if (from_name == self.d_name):
            self.saved_d = value

        v = None

        if (self.saved_d != None and
            self.saved_k != None):
            v = 3 * self.saved_d - 2 * self.saved_k
            self.clear_saved_value()

        return v



############## Helper Functions to create nodes #####################
def create_k_node(nm, from_name, days = 6, capacity = 15):
    _name = "%s_K_%d" % (from_name, days)

    if not _name in nm.nodes:
        create_rsv_node(nm, from_name, days, capacity)

        n = KNode(nm, from_name, days)
        n.capacity = capacity

        nm.nodes[_name] = n

        return n
    else:
        return nm.nodes[_name]

def create_d_node(nm, from_name, days = 6, capacity = 15):
    _name = "%s_D_%d" % (from_name, days)

    if not _name in nm.nodes:
        create_k_node(nm, from_name, days, capacity)

        n = DNode(nm, from_name, days)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]

def create_j_node(nm, from_name, days = 6, capacity = 15):
    _name = "%s_J_%d" % (from_name, days)

    if not _name in nm.nodes:
        create_d_node(nm, from_name, days, capacity)
        create_k_node(nm, from_name, days, capacity)

        n = JNode(nm, from_name, days)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]

def create_rsv_node(nm, from_name, days = 6, capacity = 15):
    rsv_name = "%s_RSV_%d" % (from_name, days)

    if not rsv_name in nm.nodes:
        basic_node.create_extreme_node(nm, from_name, days, capacity)

        rsv = RSVNode(nm, from_name, days)
        rsv.capacity = capacity

        nm.nodes[rsv_name] = rsv
        return rsv
    else:
        return nm.nodes[rsv_name]

def create_kd_node(nm, from_name, days = 6, capacity = 15):
    kd_name = "%s_KD_%d" % (from_name, days)

    if not kd_name in nm.nodes:
        create_k_node(nm, from_name, days, capacity)
        create_d_node(nm, from_name, days, capacity)

        n = KDNode(nm, from_name, days)
        n.capacity = capacity

        nm.nodes[kd_name] = n
        return n
    else:
        return nm.nodes[kd_name]

