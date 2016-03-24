from multiprocessing import Process
import time

class Aaa(Process):

	def __init__(self, aa):
		Process.__init__(self)
		self.aa = aa
		self.daemon = False

	def run(self):
		for i in range(5):
			print self.aa, i

def main():

	p_aaa = Aaa("aa")
	
	p_aaa.start()
	#p_aaa.daemon = True
	
	for i in range(5):
		print "bb", i
	
if __name__ == "__main__":
	main()