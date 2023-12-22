import core.node
import price_node
import talib
import numpy


############ KAMA nodes ###################
class KAMANode(core.node.Node):
    def __init__(self, nm, from_name, days):
        core.node.Node.__init__(self, nm, "%s_KAMA_%d" % (from_name, days))

        self.from_name = from_name
        self.days = days

        self.history_values = []

        nm.register_output_wire(from_name, self)

    def consume(self, from_name, value):
        if self.from_name != from_name:
            return None

        self.history_values.append(value)

        v = talib.KAMA(numpy.array(self.history_values, float), self.days)[-1]

        return None if numpy.isnan(v) else v


def create_kama_node(nm, from_name, days, capacity = 9):
    kama_name = "%s_KAMA_%d" % (from_name, days)

    if not kama_name in nm.nodes:
        price_node.create_price_node(nm, capacity)

        kama = KAMANode(nm, from_name, days)
        kama.capacity = capacity

        nm.nodes[kama_name] = kama

        return kama

    else:
        return nm.nodes[kama_name]
