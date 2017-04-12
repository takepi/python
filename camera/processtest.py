from multiprocessing import Process, Queue

def worker(num, q):
	for i in range(1, num):
		while q.qsize() > 0:
			q.get()
		q.put(i)

def main():
	q = Queue(maxsize = 1)
	p = Process(target = worker, args = (10000, q, ))
	p.daemon = True
	p.start()
	val = 0

	while val < 10000:
		val = q.get()

if __name__ == "__main__":
	main()