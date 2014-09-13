class Vertex(object):
	def __init__(self, name, status=0):
		self.name = name
		self.successor= []
		self.outdegree = 0
		self.indegree = 0
		self.status = status
		self.postype = 0
	def addSuccessor(self, neighbour):
		if len(self.successor) ==0 or not neighbour.name in self.successor:
			self.successor.append(neighbour.name)
			self.outdegree += 1
			neighbour.indegree += 1
	def setpostype(self, v):
		self.postype = v
	def __eq__(self, other):
		return self.name == other.name
