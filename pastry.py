from node import Node
from internet import Internet
from helper import *

class Pastry:
	def __init__(self, n):
		# self.node = Node()
		# self.n = n
		# self.internet = Internet(n)
		# self.node.connectToInternet(self.internet)
		# self.node.joinPastry()
		# self.node.print_node()

		# self.node2 = Node()
		# self.node2.connectToInternet(self.internet)
		# self.node2.joinPastry()
		# # print(self.node2.routingTable)
		# self.node2.print_node()

		# self.node3 = Node()
		# self.node3.connectToInternet(self.internet)
		# self.node3.joinPastry()

		# self.node3.print_node()

		# self.node.print_node()
		# self.node2.print_node()
		# self.node3.print_node()		

		self.internet = Internet(n)
		for x in range(n):
			node = Node()
			node.connectToInternet(self.internet)
			node.joinPastry()
		for key in self.internet.ip_data:
			self.internet.ip_data[key].print_node()
