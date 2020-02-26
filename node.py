from hashlib import md5
from codecs import encode
import hmac
from helper import *


class Node:
	def __init__(self, b=4, l=16, L=16, M=16):
		self.lessLeaf = [None]*(L//2)
		self.moreLeaf = [None]*(L//2)
		self.lessMin = None
		self.moreMax = None
		self.NeighbourSet = [None]*M
		self.routingTable = [[None]*(2**b) for x in range(l)]
		self.table = {}

	# def deliver(self, msg, key):



	def __allavailable(self):
		output = []
		for x in self.lessLeaf:
			if(x != None):
				output.append(x)

		for x in self.moreLeaf:
			if(x != None):
				output.append(x)

		for x in self.NeighbourSet:
			if(x != None):
				output.append(x)


		for x in self.routingTable:
			for y in x:
				if y!=None:
					output.append(y)
		return output


	def route(self, msg, key):
		if(self.lessMin == None and self.moreMax == None):
			# deliver(msg, key)
			print("Case 1")
			return

		if(hextoint(self.lessMin[1]) <= hextoint(key) <= hextoint(self.moreMax[1])):
			mind = abs(hextoint(self.key) - hextoint(key))
			minkey = ((self.x, self.y), self.key)

			for k in lessLeaf:
				if(k == None):
					continue
				if(abs(hextoint(k[1]) - hextoint(key)) < mind):
					mind = abs(hextoint(k[1]) - hextoint(key))
					minkey = k

			for k in moreLeaf:
				if(k == None):
					continue
				if(abs(hextoint(k[1]) - hextoint(key)) < mind):
					mind = abs(hextoint(k[1]) - hextoint(key))
					minkey = k

			if(self.key == minkey[1]):
				# deliver(msg, key)
				print("Case 2")
			else:
				return self.internet.sendmsg(msg, minkey[0])
		else:
			l = shl(key, self.key)
			j = hextoint(key[i])
			outkey = self.routingTable[l][j]
			
			if(outkey != None):
				return self.internet.sendmsg(msg, outkey[0])

			else:
				for t in __allavailable():
					if(shl(t[1], key) >= l and abs(hextoint(t[1]) - hextoint(key)) < abs(hextoint(self.key) - hextoint(key))):
						return self.internet.sendmsg(msg, t[0])

		return None


	def sendRoutingTable(self, key, ip):
		l = shl(self.key, key)
		output = []
		for i in range(l+1):
			output.append([x for x in self.routingTable[i]])

		return self.internet.sendRoutingTable(output, ip)

	def connectToInternet(self, internet):
		self.internet = internet
		self.x, self.y = self.internet.getIp(self)
		# print("My Ip: {} {}".format(self.x, self.y))

	def sendNeighbours(self):
		return [x for x in self.NeighbourSet]

	def joinPastry(self):		
		self.key = hmac.new(encode("my-secret"), msg=encode("{}, {}".format(self.x, self.y)), digestmod=md5).hexdigest()
		nearest_node = self.internet.getNearestNode(self.x, self.y)
		if(nearest_node == None):
			return 
		self.NeighbourSet = self.internet.getNeighbours(nearest_node)

		response = self.internet.sendmsg(nearest_node, "JOIN_{}".format(self.key), self.key)

				


