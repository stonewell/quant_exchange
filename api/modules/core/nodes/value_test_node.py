import core.node

class ValueTestNode(core.node.Node):
	def __init__(self, nm, from_name, delta, increase = True):
		core.node.Node.__init__(self, nm, "%s_ValueTest_%d" % (from_name, delta))

		self.from_name = from_name
		self.delta = delta
		self.increase = increase

		self.value_match = False

		nm.register_output_wire(from_name, self)

	def consume(self, from_name, value):
		if self.from_name != from_name:
			return None

		self.value_match = False

		if len(self.values) >= self.capacity - 1:
			first = self.values[0]

			if first != 0:
				change = (value - first) * 100 / first
				if (self.increase):
					self.value_match = change > self.delta 
				else: 
					self.value_match = change < self.delta
										
			else:
				self.value_match = False
		
		return value

