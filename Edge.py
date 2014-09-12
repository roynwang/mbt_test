class Edge(object):
	def __init__(self,start,end):
		self.start = start
		self.end = end
	def getStates(self):
		return (self.start, self.end)

	def __eq__(self, other):
		return self.start == other.start and self.end == other.end

