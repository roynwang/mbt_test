from Edge import *
from Vertex import *
import json
from pprint import pprint

class Graph(object):
	def __init__(self):
		self.vertexes = []
		self.edges = []
		self.degreedict = {}
	def addEdge(self, edge):
		if not edge in self.edges:
			self.edges.append(edge)
			self.updateVertex(edge)
	def updateVertex(self, edge):
		# add the vertex
		start = Vertex(edge.start)
		end = Vertex(edge.end)
		if len(self.vertexes) == 0 or not start in self.vertexes:
			self.vertexes.append(start)
		if len(self.vertexes) == 0 or not end in self.vertexes:
			self.vertexes.append(end)

		vert = self.getVertex(edge.start)
		#update the adjacency and degree
		#the in-degre of end will increment too
		vert.addAdjacency(self.getVertex(edge.end))

	def getVertex(self, name):
		for vert in self.vertexes:
			if vert.name == name:
				return vert
		return None
		
	def dump(self):
		for edge in self.edges:
			pprint(vars(edge))
		for ver in self.vertexes:
			pprint(vars(ver))

		

#this is a test
if __name__ =='__main__':
	edge1 = Edge("A","B")
	edge2 = Edge("A","C")
	edge3 = Edge("B","D")
	edge4 = Edge("C","D")
	g = Graph()
	g.addEdge(edge1)
	g.addEdge(edge2)
	g.addEdge(edge3)
	g.addEdge(edge4)
	g.dump()
