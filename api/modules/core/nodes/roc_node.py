import core.node
import price_node
import math

class ROCNode(core.node.Node):
    def __init__(self, nm, from_name, days):
        core.node.Node.__init__(self, nm, "%s_ROC_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.history_values = []

        nm.register_output_wire(from_name, self)

    def consume(self, from_name, value):
        if self.from_name != from_name:
            return None

        self.history_values.append(value)

        while len(self.history_values) > self.days + 1:
            del self.history_values[0]

        if self.history_values[0] == 0:
            return 0
            
        v = (value - self.history_values[0]) / self.history_values[0]

        return v
            
def create_roc_node(nm, from_name, days = 12, capacity = 15):
    _name = "%s_ROC_%d" % (from_name, days)

    if not _name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        n = ROCNode(nm, from_name, days)
        n.capacity = capacity

        nm.nodes[_name] = n
        return n
    else:
        return nm.nodes[_name]
