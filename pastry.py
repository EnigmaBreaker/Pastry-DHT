from node import Node
from internet import Internet
from helper import *
from collections import Counter
import random 

class Pastry:
	def __init__(self, n):
		self.internet = Internet(n)
		self.hops = []
		for x in range(n):
			hops = self.addNode()
			# print(hops)
			self.hops.append(hops)
		coll = Counter(self.hops)
		# print(coll)

		for key in self.internet.ip_data:
			self.internet.ip_data[key].print_node()
		print(coll)

		total = 0
		for key in coll:
			total += key*coll[key]
		print(total/n)
	def printPastry(self):
		for key in self.internet.ip_data:
			self.internet.ip_data[key].print_node()

	def addNode(self):
		node = Node()
		node.connectToInternet(self.internet)
		return node.joinPastry()

	def routeMsg(self, value, key=None):
		if(key == None):
			key = hex(random.randint(0, 2**32 - 1))[2:]
			# if(len(key) < 8):
			key = '0'*(8-len(key)) + key
		node = self.internet.getRandomNode()
		output, hops = node.routeMsg(key, value)
		if(output == False):
			return None
		return key, hops

	def getMsg(self, key):
		node = self.internet.getRandomNode()
		# print("Get Random Node: {}".format(node.key))
		output, hops = node.getMsg(key)
		return output, hops

	def deleteRandomNode(self):
		random_key = random.choice(list(self.internet.key_data.keys()))
		random_ip = (self.internet.key_data[random_key].x, self.internet.key_data[random_key].y)
		print("Deleting Node: {} {}".format(random_ip, random_key))

		self.internet.key_data[random_key].removeNode()
		del self.internet.key_data[random_key]
		del self.internet.ip_data[random_ip]
