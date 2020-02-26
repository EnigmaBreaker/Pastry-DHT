from node import Node
from internet import Internet
from helper import *

class Pastry:
	def __init__(self, n):
		self.node = Node()
		self.n = n
		self.internet = Internet(n)
		self.node.connectToInternet(self.internet)
		self.node.joinPastry()
		self.node2 = Node()
		self.node2.connectToInternet(self.internet)
		self.node2.joinPastry()
