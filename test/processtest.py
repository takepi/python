from multiprocessing import Process, Queue
import time

class Aaa(Process):

	def __init__(self, aa, q):
		Process.__init__(self)
		self.aa = aa
		self.q = q
		self.daemon = False

	def run(self):
		print "process start"
		for i in range(5):
			print self.aa, i
		print self.q.get()
		print "process end"

def main():

	q_aaa = Queue(maxsize = 1)

	p_aaa = Aaa("aa", q_aaa)
	q_aaa.put("avav")
	p_aaa.start()
	#p_aaa.daemon = True
	
	for i in range(5):
		print "bb", i
	
if __name__ == "__main__":
	main()