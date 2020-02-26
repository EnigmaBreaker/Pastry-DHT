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

