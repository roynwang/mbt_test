from Edge import *
from Vertex import *
import json
from pprint import pprint
import uuid

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
		#the in-degree of end will increment too
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


	#algrithem 
	#private
	#select all vertexes whose indegree is not equal outdegree
	def getTSet(self):
		TSet = []
		for v in self.vertexes:
			if v.indegree != v.outdegree:
				TSet.append(v)
		return TSet

	#To eulerize the graph, should make all vertex in TSet have the same indegre and outdegree
	def eulerize(self):	
		Tset = self.getTSet()
		while len(Tset)>0:
			#select outvex indegree>outdegree
			invex = outvex = None
			for vex in Tset:
				if vex.indegree>vex.outdegree :
					outvex = vex
					break
			#select invex indegree<outdegree and not adjacent to outvex
			for vex in Tset:
				if vex.indegree<vex.outdegree and (outvex is None or vex.name not in
						outvex.adjacencies):
					invex = vex
					break

			#create a fake vertex if there is no proper choice
			fakevex = Vertex(str(uuid.uuid1()), 1)
			if outvex is None:
				outvex = fakevex
				Tset.append(fakevex)
			elif invex is None:
				invex = fakevex
				Tset.append(fakevex)
			#create a fake edge: outvex=>invex
			#print("add edge from " + outvex.name + " to " +  invex.name)
			self.addEdge(Edge(outvex.name, invex.name, 1))

			#remove the vertex from Tset if the indegree == outdegree
			for vex in [outvex, invex]:
				if vex.indegree == vex.outdegree :
					#print("remove " + vex.name)
					Tset.remove(vex)

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
	g.eulerize()
	g.dump()
