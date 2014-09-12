from Vertex import *


class Edge(object):
	#status:0 => normal 
	#status:1 => fake
	#status:2 => hide
	def __init__(self,start,end,status=0):
		#support str/Vertex parameters
		if isinstance(start, Vertex):
			start = start.name
		if isinstance(end, Vertex):
			end = end.name
		self.start = start
		self.end = end
		self.status = status
	def getStates(self):
		return (self.start, self.end)
	def __eq__(self, other):
		return self.start == other.start and self.end == other.end

