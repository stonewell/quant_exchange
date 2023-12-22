import core.node
import price_node
import math
from general_osc_node import GeneralOSCNode

########### Crest node for days ###############
class CrestNode(core.node.Node):
    def __init__(self, nm, from_name, days = 3):
        '''
        days: how much days to be tested before/after to identify crest
        '''
        core.node.Node.__init__(self, nm, "%s_Crest_%d" % (from_name, days), days * 2 + 1)

        self.from_name = from_name
        self.days = days
        self.from_values = []

        nm.register_output_wire(from_name, self)

    def consume(self, from_name, value):
        self.from_values.append(value)

        if len(self.from_values) < self.days * 2 + 1:
            return 0

        while len(self.from_values) > self.days * 2 + 1:
            del self.from_values[0]

        is_crest = (all(x <= self.from_values[self.days] for x in self.from_values) and
                    any(x < self.from_values[self.days] for x in self.from_values[0:self.days]) and
                    any(x < self.from_values[self.days] for x in self.from_values[self.days + 1:]))

        return 1 if is_crest else 0
 
########### Trough node for days ###############
class TroughNode(core.node.Node):
    def __init__(self, nm, from_name, days = 3):
        '''
        days: how much days to be tested before/after to identify trough
        '''
        core.node.Node.__init__(self, nm, "%s_Trough_%d" % (from_name, days), days * 2 + 1)

        self.from_name = from_name
        self.days = days
        self.from_values = []

        nm.register_output_wire(from_name, self)

    def consume(self, from_name, value):
        self.from_values.append(value)

        if len(self.from_values) < self.days * 2 + 1:
            return 0

        while len(self.from_values) > self.days * 2 + 1:
            del self.from_values[0]

        is_trough = (all(x >= self.from_values[self.days] for x in self.from_values) and
                    any(x > self.from_values[self.days] for x in self.from_values[0:self.days]) and
                    any(x > self.from_values[self.days] for x in self.from_values[self.days + 1:]))

        return 1 if is_trough else 0

################## callback node #########################
class CallbackNode(core.node.Node):
    def __init__(self, nm, node, callback):
        core.node.Node.__init__(self, nm, "%s_Callback" % (node.name), 1)

        self.callback = callback
        self.node = node
        nm.register_output_wire(node.name, self)

    def consume(self, from_name, value):
        self.callback(self.node, from_name, value)

        return None
            
################## Helper functions to create basic node ######################
def create_crest_node(nm, from_name, days = 3, capacity = 7):
    name = "%s_Crest_%d" % (from_name, days)

    if not name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        crest = CrestNode(nm, from_name, days)
        crest.capacity = capacity
        nm.nodes[name] = crest

        return crest
    else:
        return nm.nodes[name]

def create_trough_node(nm, from_name, days = 3, capacity = 7):
    name = "%s_Trough_%d" % (from_name, days)

    if not name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        trough = TroughNode(nm, from_name, days)
        trough.capacity = capacity
        nm.nodes[name] = trough

        return trough
    else:
        return nm.nodes[name]

def create_crest_node_with_callback(call_back, nm, from_name, days = 3, capacity = 7):
    crest = create_crest_node(nm, from_name, days, capacity)

    callback_node = CallbackNode(nm, crest, call_back)

def create_trough_node_with_callback(call_back, nm, from_name, days = 3, capacity = 7):
    trough = create_trough_node(nm, from_name, days, capacity)

    callback_node = CallbackNode(nm, trough, call_back)
