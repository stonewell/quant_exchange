
class Node(object):
	def __init__(self, nm, name, capacity = 15):
		self.nm = nm
		self.name = name
		self.capacity = capacity
		self.values = []

	def consume(self, from_name, value):
		"""
		All subclass need to override this function to do 
		acturlly calculation
		"""
		pass

	def data_income(self, from_name, value):
		out_val = self.consume(from_name, value)

		if out_val != None:
			self.values.append(out_val)
			
			while len(self.values) > self.capacity:
				del self.values[0]

			self.data_output(self.name, out_val)
			
	def data_output(self, from_name, value):
		if from_name in self.nm.output_wires:
			wires = self.nm.output_wires[from_name]
			for wired_node in wires:
				wired_node.data_income(from_name, value)

	def snapshot(self):
		return [v for v in self.values]
