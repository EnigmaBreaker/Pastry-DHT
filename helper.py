import math

def proximityDistance(x1, y1, x2, y2):
	return max(abs(x1 - x2), abs(y1 - y2))

def hextoint(s):
	return int('0x'+s, 0)

def shl(a, b):
	output = 0
	for i in range(len(a)):
		if(a[i] == b[i]):
			output+=1
		else:
			break

	return output

def findmin(arr):
	output = None
	ind = 0
	for i, x in enumerate(arr):
		if output == None:
			output = x
			ind = i
		elif(x != None and hextoint(output[1]) > hextoint(x[1])):
			output = x
			ind = i
	return output, ind

def findmax(arr):
	output = None
	ind = 0
	for i, x in enumerate(arr):
		if output == None:
			output = x
			ind = i
		elif(x != None and hextoint(output[1]) < hextoint(x[1])):
			output = x
			ind = i
	return output, ind

def findClosest(valid, key):
	minDistance = math.inf 
	minNode = None

	for node in valid:
		if(abs(hextoint(node[1]) - hextoint(key)) < minDistance):
			minNode = node
			minDistance = abs(hextoint(node[1]) - hextoint(key))

	return minNode

def findProximityClosest(arr, x, y):
	output = None
	mindis = math.inf 
	minind = -1
	for i, a in enumerate(arr):
		if(a == None):
			continue
		ip, key = a
		# print(ip, key)
		dis = proximityDistance(ip[0], ip[1], x, y)
		if(dis < mindis):
			mindis = dis
			output = (ip, key)
			minind = i

	return output, minind
