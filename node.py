from hashlib import sha1
from codecs import encode
import hmac
from helper import *
import math


class Node:
	def __init__(self, b=4, l=8, L=16, M=32):
		self.lessLeaf = [None]*(L//2)
		self.moreLeaf = [None]*(L//2)
		self.neighbourSet = [None]*M
		self.routingTable = [[None]*(2**b) for x in range(l)]
		self.table = {}
		self.l = l 
		self.L = L 
		self.M = M
		self.b = b 


	def print_arr(self, arr):
		print("|", end=" ")
		for x in arr:
			if x == None:
				print(x, end="     | ")
			else:
				print(x[1], end=" | ")
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

		print("[@] Neighbor Set")
		print(self.neighbourSet)

		print()

		# print("[@] Routing Table: ")
		# for x in self.routingTable:
		# 	self.print_arr(x)
		self.print_routing()
		print()
		print()
		print()
		
	def print_routing(self):
		print("Routing table. ID: {}".format(self.key))
		print()
		print("|" + "-"*(11*16 - 1) + "|")
		# print()
		for x in self.routingTable:
			self.print_arr(x)
		print("|" + "-"*(11*16 - 1) + "|")

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

	def parseMsg(self, msg, key, source_ip):
		if(msg[0:4] == "JOIN" and msg.split("_")[-1] == key):
			self.sendLeafSet(source_ip)
			output = True
		elif(msg[0:4] == "FIND" and msg.split("_")[-1] == key):
			if key in self.table:
				return self.table[key]
			else:
				return False
		else:
			if key in self.table:
				return False
			else:
				self.table[key] = msg
				return True
			# self.internet.sendResponse(source_ip)

	def route(self, msg, key, source_ip, hops):
		self.msgCheck(msg, key, source_ip)
		# print(hops)
		minleaf, ind = findmin(self.lessLeaf)
		maxleaf, ind = findmax(self.moreLeaf)

		if(minleaf == None and maxleaf == None):
			output = self.parseMsg(msg, key, source_ip)
			# self.sendLeafSet(source_ip)
			# print("Case 1")
			return output, hops

		if(minleaf == None):
			minleaf = ((self.x, self.y), self.key)
		if(maxleaf == None):
			maxleaf = ((self.x, self.y), self.key)

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
				output = self.parseMsg(msg, key, source_ip)
				# self.sendLeafSet(source_ip)
				# print("Case 2")
				return output, hops
			else:
				return self.internet.sendmsg(minkey[0], msg, key, source_ip, hops+1)
		else:
			l = shl(key, self.key)
			j = hextoint(key[l])
			outkey = self.routingTable[l][j]
			
			if(outkey != None):
				return self.internet.sendmsg(outkey[0], msg, key, source_ip, hops+1)

			else:
				for t in self.__allavailable():
					if(shl(t[1], key) >= l and abs(hextoint(t[1]) - hextoint(key)) < abs(hextoint(self.key) - hextoint(key))):
						return self.internet.sendmsg(t[0], msg, key, source_ip, hops+1)
		# print("Case 3 - Inside Node {} {}".format(self.x, self.y))
		output = self.parseMsg(msg, key, source_ip)
		# print(hops)
		return output, hops
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
			if(i != l):
				output.append([])
				continue
			output.append([x for x in self.routingTable[i]])
			output[i][hextoint(self.key[i])] = ((self.x, self.y), self.key)

		return self.internet.sendRoutingTable(output, ip)

	def getRoutingTable(self, table):
		for i, x in enumerate(table):
			if(i != len(table) - 1):
				continue
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
			"ip" : (self.x, self.y)
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

		if((minLeaf == None or hextoint(key) > hextoint(minLeaf[1])) and hextoint(self.key) > hextoint(key)):
			self.lessLeaf[i1] = (ip, key)
		
		if((maxLeaf == None or hextoint(key) < hextoint(maxLeaf[1])) and hextoint(self.key) < hextoint(key)):
			self.moreLeaf[i2] = (ip, key)



	def getState(self, payload):
		# for x in payload["routingTable"]:
		# 	for y in x:
		# 		if(y != None):
		self.updateRoutingTable(payload["ip"], payload["key"])
		self.updateLeafSet(payload["ip"], payload["key"])
		self.updateNeighbour(payload["ip"], payload["key"])
		
	def updateNeighbour(self, ip, key):
		if None in self.neighbourSet:
			ind = self.neighbourSet.index(None)
			self.neighbourSet[ind] = (ip, key)
			return

		distance = proximityDistance(ip[0], ip[1], self.x, self.y)
		max_dis = distance
		max_ind = -1
		for i, x in enumerate(self.neighbourSet):
			dis_curr = proximityDistance(x[0][0], x[0][1], self.x, self.y)
			if dis_curr > max_dis:
				max_dis = dis_curr
				max_ind = i

		if(max_ind != -1):
			self.neighbourSet[max_ind] = (ip, key)
		

	def joinPastry(self):	
		self.key = hmac.new(encode("my-secret"), msg=encode("{}, {}".format(self.x, self.y)), digestmod=sha1).hexdigest()[:self.l]
		self.internet.updateKeyData(self)
		nearest_node = self.internet.getNearestNode(self.x, self.y)
		if(nearest_node == None):
			return 0
		self.neighbourSet = self.internet.getNeighbours(nearest_node[0])
		self.updateNeighbour(nearest_node[0], nearest_node[1])
		output, hops = self.internet.sendmsg(nearest_node[0], "JOIN_{}".format(self.key), self.key, (self.x, self.y), 0)
		# print(hops)
		all_nodes = self.__allavailable()

		for node in all_nodes:
			self.sendState(node[0])

		return hops

	def routeMsg(self, key, value):
		output, hops = self.route(value, key, (self.x, self.y), 0)
		return output, hops

	def getMsg(self, key):
		output, hops = self.route("FIND_{}".format(key), key, (self.x, self.y), 0)
		return output, hops

	def deleteLeaf(self, ip, key):
		if (ip, key) in self.lessLeaf:
			ind = self.lessLeaf.index((ip, key))
			self.lessLeaf[ind] = None

			minnode, minind = findmin(self.lessLeaf)
			if(minnode != None):
				minnode = self.internet.key_data[minnode[1]]
				more, less = minnode.moreLeaf, minnode.lessLeaf

				valid = []
				for leaf in more+less:
					if(leaf == None):
						continue
					if(leaf not in self.lessLeaf and leaf[1] < self.key and leaf[1] != key):
						valid.append(leaf)

				closest = findClosest(valid, self.key)
				self.lessLeaf[ind] = closest

		if (ip, key) in self.moreLeaf:
			ind = self.moreLeaf.index((ip, key))
			self.moreLeaf[ind] = None

			maxnode, maxind = findmax(self.moreLeaf)
			if(maxnode != None):
				maxnode = self.internet.key_data[maxnode[1]]
				more, less = maxnode.moreLeaf, maxnode.lessLeaf

				valid = []
				for leaf in more+less:
					if(leaf == None):
						continue
					if(leaf not in self.moreLeaf and leaf[1] < self.key and leaf[1] != key):
						valid.append(leaf)

				closest = findClosest(valid, self.key)
				self.moreLeaf[ind] = closest


	def deleteNeighbour(self, ip, key):
		if (ip, key) in self.neighbourSet:
			ind = self.neighbourSet.index((ip, key))
			self.neighbourSet[ind] = None

			minnode, minind = findProximityClosest(self.neighbourSet, self.x, self.y)

			if(minnode != None):
				minnode = self.internet.key_data[minnode[1]]
				neighbours = minnode.neighbourSet
				valid = []
				for neighbour in neighbours:
					if(neighbour == None):
						continue
					if(neighbour not in self.neighbourSet and neighbour[1] != self.key and neighbour[1] != key):
						valid.append(neighbour)
				closest, ind = findProximityClosest(valid, self.x, self.y)
				self.neighbourSet[minind] = closest


	def findNewRouting(self, row, col, sourcekey):
		for i in range(row, self.l):
			for j in range(self.L):
				if(j == col):
					continue
				if(self.routingTable[i][j] == None):
					continue
				ip, key = self.routingTable[i][j]
				if(key == sourcekey):
					continue
				newNode = self.internet.ip_data[ip]
				if(newNode.routingTable[row][col] != None):
					if(newNode.routingTable[row][col][1] != sourcekey):
						self.routingTable[row][col] = newNode.routingTable[row][col]
						return



	def deleteRoutingTable(self, ip, key):
		for i, row in enumerate(self.routingTable):
			for j, col in enumerate(row):
				if(col == None):
					continue
				if(col[1] != key):
					continue
				self.routingTable[i][j] = None
				self.findNewRouting(i, j, key)



	def deleteEntry(self, ip, key):
		self.deleteLeaf(ip, key)
		self.deleteNeighbour(ip, key)
		self.deleteRoutingTable(ip, key)


	def removeNode(self):
		nodes = self.internet.getAllNodes()
		for node in nodes:
			node.deleteEntry((self.x, self.y), self.key)

