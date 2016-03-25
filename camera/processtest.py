from multiprocessing import Process, Queue
import time

def worker(num, q):
	for i in range(1, num):
		while q.qsize() > 0:
			q.get()
		q.put(i)
		time.sleep(0.01)
#		print "put", i
"""
def getq(q):
	print "get"
	time.sleep(1)
	if q.empty() == True:
		print "empty"
	else:
		print q.get(), "get"
"""
q = Queue(maxsize = 1)
p = Process(target = worker, args = (10000, q, ))
#g = Process(target = getq, args = (q, ))
p.daemon = True
#g.daemon = True
p.start()
#g.start()
while True:
	print q.get()
	time.sleep(0.1)
