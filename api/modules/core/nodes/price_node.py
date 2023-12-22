import core.node

class PriceNode(core.node.Node):
	def __init__(self, nm, capacity = 15):
		core.node.Node.__init__(self, nm, "Price", capacity)

		nm.register_output_wire("", self)

	def data_income(self, from_name, value):
		if from_name != "":
			return

		self.values.append(value)
			
		while len(self.values) > self.capacity:
			del self.values[0]

		self.data_output("Close", value.close_price)
		self.data_output("Amount", value.amount)
		self.data_output("Lowest", value.lowest_price)
		self.data_output("Highest", value.highest_price)
		self.data_output("Open", value.open_price)

def create_price_node(nm, capacity = 15):
	if not "Price" in nm.nodes:
		price = PriceNode(nm, capacity)
		
		nm.nodes["Price"] = price

		return price
	else:
		return nm.nodes["Price"]
