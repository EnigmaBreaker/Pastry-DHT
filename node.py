from hashlib import md5
from codecs import encode
import hmac

class Node:
	def __init__(self, b=4, l=16, L=16, M=16):
		self.leftLeaf = [None]*(L//2)
		self.rightLeaf = [None]*(L//2)
		self.NeighbourSet = [None]*M
		self.routingTable = [[None]*(2**b) for x in range(l)]
		self.table = {}


	def connectToInternet(self, internet):
		self.internet = internet
		self.x, self.y = self.internet.getIp(self)

	def joinPastry(self, internet):
		try:
			self.key = hmac.new(encode("my-secret"), msg=encode("{}, {}".format(self.x, self.y)), digestmod=md5).hexdigest()
			self.internet.addToPastry(self.key)
		except:
			print("Not connected to internet")


if __name__ == "__main__":
	node = Node(2, 3)
	print(node.leftLeaf)
	print(node.rightLeaf)
	print(node.NeighbourSet)
	print(node.routingTable)
	# print(node.key)