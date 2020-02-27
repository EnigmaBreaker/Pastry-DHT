from hashlib import md5
from codecs import encode
import hmac
from helper import *


class Node:
	def __init__(self, b=4, l=8, L=16, M=16):
		self.lessLeaf = [None]*(L//2)
		self.moreLeaf = [None]*(L//2)
		self.neighbourSet = [None]*M
		self.routingTable = [[None]*(2**b) for x in range(l)]
		self.table = {}

	def print_arr(self, arr):
		for x in arr:
			if x == None:
				print(x, end="     ")
			else:
				print(x[1], end=" ")
		print()

	def print_node(self):
		print("||||||| --- Printing status of Node with IP: ({}, {}) and Key: {} --- |||||||".format(self.x, self.y, self.key))
		print()
		print("[@] Less Leaf")
		self.print_arr(self.lessLeaf)
		print()

		print("[@] More Leaf")
		self.print_arr(self.moreLeaf)

		print()

		print("[@] Neighbour Set")
		print(self.neighbourSet)

		print()

		print("[@] Routing Table: ")
		for x in self.routingTable:
			self.print_arr(x)

		print()
		print()
		print()
		
		

	def __allavailable(self):
		output = set()
		for x in self.lessLeaf:
			if(x != None):
				output.add(x)

		for x in self.moreLeaf:
			if(x != None):
				output.add(x)

		for x in self.neighbourSet:
			if(x != None):
				output.add(x)


		for x in self.routingTable:
			for y in x:
				if y!=None:
					output.add(y)
		return output


	def msgCheck(self, msg, key, source_ip):
		if(msg[0:4] == "JOIN" and msg.split("_")[-1] == key):
			self.sendRoutingTable(key, source_ip)

	def route(self, msg, key, source_ip):
		self.msgCheck(msg, key, source_ip)

		minleaf, ind = findmin(self.lessLeaf)
		maxleaf, ind = findmax(self.moreLeaf)

		if(minleaf == None):
			minleaf, ind = findmin(self.moreLeaf)
		if(maxleaf == None):
			maxleaf, ind = findmax(self.lessLeaf)

		if(minleaf == None and maxleaf == None):
			self.sendLeafSet(source_ip)
			# print("Case 1")
			return

		if(hextoint(minleaf[1]) <= hextoint(key) <= hextoint(maxleaf[1])):
			mind = abs(hextoint(self.key) - hextoint(key))
			minkey = ((self.x, self.y), self.key)

			for k in self.lessLeaf:
				if(k == None):
					continue
				if(abs(hextoint(k[1]) - hextoint(key)) < mind):
					mind = abs(hextoint(k[1]) - hextoint(key))
					minkey = k

			for k in self.moreLeaf:
				if(k == None):
					continue
				if(abs(hextoint(k[1]) - hextoint(key)) < mind):
					mind = abs(hextoint(k[1]) - hextoint(key))
					minkey = k

			if(self.key == minkey[1]):
				self.sendLeafSet(source_ip)
				# print("Case 2")
				return
			else:
				return self.internet.sendmsg(minkey[0], msg, key, source_ip)
		else:
			l = shl(key, self.key)
			j = hextoint(key[l])
			outkey = self.routingTable[l][j]
			
			if(outkey != None):
				return self.internet.sendmsg(outkey[0], msg, key, source_ip)

			else:
				for t in self.__allavailable():
					if(shl(t[1], key) >= l and abs(hextoint(t[1]) - hextoint(key)) < abs(hextoint(self.key) - hextoint(key))):
						return self.internet.sendmsg(t[0], msg, key, source_ip)
		# print("Case 3 - Inside Node {} {}".format(self.x, self.y))
		self.sendLeafSet(source_ip)
		# return None

	def sendLeafSet(self, ip):
		less_temp = [x for x in self.lessLeaf]
		more_temp = [x for x in self.moreLeaf]
		self.internet.sendLeafSet(ip, less_temp, more_temp, (self.x, self.y), self.key)

	def getLeafSet(self, lessLeaf, moreLeaf, ip, key):

		self.lessLeaf = [x for x in lessLeaf]
		self.moreLeaf = [x for x in moreLeaf]


		if None in self.lessLeaf:
			ind = self.lessLeaf.index(None)
			if(hextoint(self.key) > hextoint(key)):
				self.lessLeaf[ind] = (ip, key)
				return

		if None in self.moreLeaf:
			ind = self.moreLeaf.index(None)
			if(hextoint(self.key) < hextoint(key)):
				self.moreLeaf[ind] = (ip, key)
				return

		maxmore, i1 = findmax(self.moreLeaf)
		minless, i2 = findmax(self.lessLeaf)


		if((minless == None or hextoint(key) > hextoint(minless[1])) and hextoint(self.key) > hextoint(key)):
			self.lessLeaf[i2] = (ip, key)
		
		if((maxmore == None or hextoint(key) < hextoint(maxmore[1])) and hextoint(self.key) < hextoint(key)):
			self.moreLeaf[i1] = (ip, key)
		

		
	def sendRoutingTable(self, key, ip):
		l = shl(self.key, key)
		output = []
		for i in range(l+1):
			output.append([x for x in self.routingTable[i]])
			output[i][hextoint(self.key[i])] = ((self.x, self.y), self.key)

		return self.internet.sendRoutingTable(output, ip)

	def getRoutingTable(self, table):
		for i, x in enumerate(table):
			for j, y in enumerate(x):
				if(self.routingTable[i][j] == None):
					self.routingTable[i][j] = table[i][j]

			self.routingTable[i][hextoint(self.key[i])] = None
		return True

	def connectToInternet(self, internet):
		self.internet = internet
		self.x, self.y = self.internet.getIp(self)
		# print("My Ip: {} {}".format(self.x, self.y))

	def sendNeighbours(self):
		return [x for x in self.neighbourSet]

	def sendState(self, ip):
		temp_routing = []
		for i, x in enumerate(self.routingTable):
			temp_routing.append([y for y in x])
			temp_routing[i][hextoint(self.key[i])] = ((self.x, self.y), self.key)

		payload = {
			"key" : self.key,
			"ip" : (self.x, self.y),
			"lessLeaf" : [x for x in self.lessLeaf],
			"moreLeaf" : [x for x in self.moreLeaf],
			"neighbourhoodSet" : [x for x in self.neighbourSet], 
			"routingTable" : temp_routing
		}

		self.internet.sendState(ip, payload)

	def updateRoutingTable(self, ip, key):
		if(key != self.key):
			l = shl(self.key, key)
			j = hextoint(key[l])
			if(self.routingTable[l][j] == None):
				self.routingTable[l][j] = (ip, key)

	def updateLeafSet(self, ip, key):

		if None in self.lessLeaf:
			ind = self.lessLeaf.index(None)
			if(hextoint(self.key) > hextoint(key)):
				self.lessLeaf[ind] = (ip, key)
				return

		if None in self.moreLeaf:
			ind = self.moreLeaf.index(None)
			if(hextoint(self.key) < hextoint(key)):
				self.moreLeaf[ind] = (ip, key)
				return

		minLeaf, i1 = findmin(self.lessLeaf)
		maxLeaf, i2 = findmax(self.moreLeaf)

		if(minLeaf == None):
			minLeaf, i1 = findmin(self.moreLeaf)

		if(maxLeaf == None):
			maxLeaf, i2 = findmax(self.lessLeaf)

		if((minLeaf == None or hextoint(key) > hextoint(minLeaf[1])) and hextoint(self.key) > hextoint(key)):
			self.lessLeaf[i2] = (ip, key)
		
		if((maxLeaf == None or hextoint(key) < hextoint(maxLeaf[1])) and hextoint(self.key) < hextoint(key)):
			self.moreLeaf[i1] = (ip, key)



	def getState(self, payload):
		for x in payload["routingTable"]:
			for y in x:
				if(y != None):
					self.updateRoutingTable(y[0], y[1])
		
		self.updateLeafSet(payload["ip"], payload["key"])
		
		
		

	def joinPastry(self):	
		self.key = hmac.new(encode("my-secret"), msg=encode("{}, {}".format(self.x, self.y)), digestmod=md5).hexdigest()[:8]
		nearest_node = self.internet.getNearestNode(self.x, self.y)
		if(nearest_node == None):
			return 
		self.neighbourSet = self.internet.getNeighbours(nearest_node)

		self.internet.sendmsg(nearest_node, "JOIN_{}".format(self.key), self.key, (self.x, self.y))

		all_nodes = self.__allavailable()

		for node in all_nodes:
			self.sendState(node[0])
				


