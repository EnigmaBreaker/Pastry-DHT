
class Internet:
	def __init__(self, n):
		self.grid = [[None for x in range(n)] for y in range(n)]
		self.ip_data = {}
	def getIp(self, node):
		self.ip_data[(0, 0)] = node
		return 0, 0