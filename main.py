from node import Node 
from internet import Internet
from pastry import Pastry
import sys


def test1(pastry, numiters):
	keys = []

	i = 0
	while(i < numiters):
		key = pastry.routeMsg(str(i))
		if not key:
			print("Error")
			continue
		# if key[0] in keys:
		# 	print("Duplicate")
		# 	continue
		else:
			if(i % 1000 == 0):
				print("Appending Key, value: {}, {}".format(key[0], i))
			keys.append(key[0])
			i+=1

	print("Checking status")
	wrong = 0
	for i in range(numiters):
		# wrong = 0
		output, hops = pastry.getMsg(keys[i])
		if(output == False):
			# print("Checking status: {} Errrrror1".format(keys[i]))
			wrong+=1
			# break
		elif(output == str(i)):
			# pass
			if(i % 1000 == 0):
				print("Checking status: {} {} Yipeeeeee".format(keys[i], i))
		else:
			print("Checking status: {} {} Errrrror2".format(keys[i], i))
	print("wrong ones: {}".format(wrong))

if __name__ == "__main__":
	pastry = Pastry(int(sys.argv[1]))
	for i in range(int(sys.argv[1])//2):
		pastry.deleteRandomNode()
		# pastry.printPastry()
	test1(pastry, 1000000)