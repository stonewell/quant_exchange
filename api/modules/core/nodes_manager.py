import utils.list_utils

class NodesManager(object):
	def __init__(self):
		self.output_wires = {}
		self.nodes = {}

	def register_output_wire(self, name, node):
		if name in self.output_wires:
			wired_nodes = self.output_wires[name]
			
			if not utils.list_utils.contains(wired_nodes, node):
				wired_nodes.append(node)
		else:
			wired_nodes = [node]
			self.output_wires[name] = wired_nodes

	
	def unregister_output_wire(self, name, node):
		if name in self.output_wires:
			wired_nodes = self.output_wires[name]

			utils.list_utils.del_noerr(wired_nodes, node)

				
