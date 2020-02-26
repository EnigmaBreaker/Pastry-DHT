def proximityDistance(x1, y1, x2, y2):
	return max(abs(x1 - x2), abs(y1 - y2))

def hextoint(s):
	return int('0x'+s, 0)

def shl(self, a, b):
	output = 0
	for i in range(len(key)):
		if(a[i] == b[i]):
			output+=1
		else:
			break

	return output