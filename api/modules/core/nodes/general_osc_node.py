import core.node

generate_predict_osc_value = True

print '************************* OSC Node will generate predict value:', generate_predict_osc_value, '******************************'

def default_norm_func(v):
    if generate_predict_osc_value and v != 0:
        v = int(v / 10) * 10
        if v < 0:
            v -= 1
        else:
            v += 1

    return v

class GeneralOSCNode(core.node.Node):
    def __init__(self, nm, name, from_name1, from_name2, delta_only = False,
                 norm_func = default_norm_func):
        core.node.Node.__init__(self, nm, name)
        
        self.ma_name1 = from_name1
        self.ma_name2 = from_name2
        self.delta_only = delta_only
        self.norm_func = norm_func

        nm.register_output_wire(self.ma_name1, self)
        nm.register_output_wire(self.ma_name2, self)

        self.clear_saved_value()

    def clear_saved_value(self):
        self.ma_v1 = None
        self.ma_v2 = None

    def consume(self, from_name, value):
        if self.ma_name1 == from_name:
            self.ma_v1 = value

        if self.ma_name2 == from_name:
            self.ma_v2 = value

        v = None

        if (self.ma_v1 != None and
            self.ma_v2 != None):
            if self.delta_only:
                v = self.ma_v1 - self.ma_v2
            elif self.ma_v1 == 0:
                v = 0
            else:
                v = (self.ma_v1 - self.ma_v2) / self.ma_v1 * 100

            if self.norm_func is not None:
                v = self.norm_func(v)
            self.clear_saved_value()

        return v
#end class General OSCNode
