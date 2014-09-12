class Vertex(object):
	def __init__(self, name):
		self.name = name
		self.adjacencies= []
		self.outdegree = 0
		self.indegree = 0
	def addAdjacency(self, neighbour):
		if len(self.adjacencies) ==0 or not neighbour.name in self.adjacencies:
			self.adjacencies.append(neighbour.name)
			self.outdegree += 1
			neighbour.indegree += 1
	def removeAdjaceny(self,neighbour):
		self.adjacencies.remove(neighbour.name)
		self.outdegree -= 1
		neighbour.indegree -= 1
	def __eq__(self, other):
		return self.name == other.name
