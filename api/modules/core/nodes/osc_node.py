import core.node
import basic_node
from general_osc_node import GeneralOSCNode, default_norm_func
                    
class OSCNode(GeneralOSCNode):
    def __init__(self, nm, from_name, days1 = 12, days2 = 26):
        GeneralOSCNode.__init__(self, nm,
                                "%s_OSC_%d_%d" % (from_name, days1, days2),
                                "%s_MA_%d" % (from_name, days1),
                                "%s_MA_%d" % (from_name, days2),
                                norm_func = self.osc_norm_func)
        self.from_name = from_name
        
    def osc_norm_func(self, v):
        if self.from_name == 'Close':
            return int(v)

        return default_norm_func(v)
#end class OSCNode
        
def create_osc_node(nm, from_name, days1 = 12, days2 = 26, capacity = 15):
    _name = "%s_OSC_%d_%d" % (from_name, days1, days2)

    if not _name in nm.nodes:
        basic_node.create_ma_node(nm, from_name, days1, capacity)
        basic_node.create_ma_node(nm, from_name, days2, capacity)

        n = OSCNode(nm, from_name, days1, days2)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]
