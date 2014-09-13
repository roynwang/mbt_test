from Vertex import *


class Edge(object):
	#status:0 => normal 
	#status:1 => fake
	def __init__(self,start,end,status=0):
		#support str/Vertex parameters
		if isinstance(start, Vertex):
			self.start = start
		else:
			self.start = Vertex(start)
		if isinstance(end, Vertex):
			self.end = end
		else:
			self.end = Vertex(end)
		self.status = status
		self.hitted = 0

	def getStates(self):
		return (self.start, self.end)

	def hit(self):
		self.hitted = 1
	def dump(self):
		print(str(self.status) + ": " + self.start.name + " => " + self.end.name) 
	def __eq__(self, other):
		return self.start == other.start and self.end == other.end

