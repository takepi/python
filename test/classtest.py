class A:
#	def __init__(self):
#		self.a = 1
		
	def tasu(self, n):
		self.a = n
		
	def get(self):
		return self.a
		
a = A()
a.tasu(1)
print a.get()
a.tasu(2)
print a.get()