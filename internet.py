import random
from helper import *

class Internet:
	def __init__(self, n):
		if(n % 2 == 0):
			n += 1
		self.grid = [[None for x in range(n)] for y in range(n)]
		self.ip_data = {}
		self.key_data = {}
		self.n = n

	def __scanring(self, x, y, i):
		x1 = (x - i) % self.n
		x2 = (x + i) % self.n
		y1 = (y - i) % self.n
		y2 = (y + i) % self.n

		for j in range(2*i + 1):
			curr_x = (x1 + j)%self.n
			curr_y = y1

			# print(curr_x, curr_y)

			if (curr_x, curr_y) in self.ip_data:
				return ((curr_x, curr_y), self.ip_data[(curr_x, curr_y)].key)

		for j in range(1, 2*i + 1):
			curr_x = x2
			curr_y = (y1 + j)%self.n

			# print(curr_x, curr_y)

			if (curr_x, curr_y) in self.ip_data:
				return ((curr_x, curr_y), self.ip_data[(curr_x, curr_y)].key)

		for j in range(1, 2*i + 1):
			curr_x = (x2 - j)%self.n
			curr_y = y2

			# print(curr_x, curr_y)

			if (curr_x, curr_y) in self.ip_data:
				return ((curr_x, curr_y), self.ip_data[(curr_x, curr_y)].key)

		for j in range(1, 2*i):
			curr_x = x1
			curr_y = (y2 - j)%self.n

			# print(curr_x, curr_y)

			if (curr_x, curr_y) in self.ip_data:
				return ((curr_x, curr_y), self.ip_data[(curr_x, curr_y)].key)
		return None


	def getNearestNode(self, x, y):
		# print("Scanning with {} {}".format(x, y))
		for i in range(self.n//2):
			curr = self.__scanring(x, y, i+1)
			if(curr != None):
				return curr 

		return None
		
	def getRandomNode(self):
		ip = random.choice(list(self.ip_data.keys()))
		return self.ip_data[ip]

	def getNeighbours(self, ip):
		return self.ip_data[ip].sendNeighbours()

	def getIp(self, node):
		while(True):
			curr = random.randint(0, self.n**2-1)
			x = curr//self.n
			y = curr%self.n
			if (x, y) not in self.ip_data:
				break

		self.ip_data[(x, y)] = node
		return x, y

	def updateKeyData(self, node):
		self.key_data[node.key] = node



	def sendmsg(self, ip, msg, key, source_ip, hops):
		out = self.ip_data[ip].route(msg, key, source_ip, hops)
		# print(out)
		return out
	def sendRoutingTable(self, table, ip):
		return self.ip_data[ip].getRoutingTable(table)

	def sendLeafSet(self, ip, lessLeaf, moreLeaf, sourceip, sourcekey):
		return self.ip_data[ip].getLeafSet(lessLeaf, moreLeaf, sourceip, sourcekey)

	def sendState(self, ip, payload):
		return self.ip_data[ip].getState(payload)

	def getAllNodes(self):
		nodes = []
		for ip in self.ip_data:
			nodes.append(self.ip_data[ip])

		return nodes

