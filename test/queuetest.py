from Queue import LifoQueue

q = LifoQueue()

for i in range(5):
	q.put(i)
	print "put: ", i

while True:
	if q.empty():
		break
	else:
		i = q.get(timeout = 1)
		print "get :", i