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
		vert.addSuccessor(self.getVertex(edge.end))

	def getVertex(self, name):
		for vert in self.vertexes:
			if vert.name == name:
				return vert
		return None
	def setVexPtype(self, name, ptype):
		self.getVertex(name).setpostype(ptype)

	def getEdge(self, start, end, hitted = None):
		for edge in self.edges:
			if edge.start == start  and edge.end == end and (hitted is None or edge.hitted == hitted):
				return edge
		return None

	def getStartVex(self):
		ret = []
		for vex in self.vertexes:
			if vex.postype & 1 != 0:
				ret.append(vex)
		return ret
	def getEndVex(self):
		ret = []
		for vex in self.vertexes:
			if vex.postype & 2 != 0:
				ret.append(vex)
		return ret

		
	def dump(self):
		for edge in self.edges:
			pprint(vars(edge))
		print("================")
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
						outvex.successor):
					invex = vex
					break

			#create a fake vertex if there is no proper choice
			fake = None
			if outvex is None:
				fake = outvex = Vertex(str(uuid.uuid1()), 1)
			elif invex is None:
				fake = invex = Vertex(str(uuid.uuid1()), 1)

			#create a fake edge: outvex=>invex
			print("add edge from " + outvex.name + " to " +  invex.name)
			self.addEdge(Edge(outvex.name, invex.name, 1))

			#update fake status: SHOULD mark it as a fake vertex
			if not fake is None:
				self.getVertex(fake.name).status = 1

			#remove the vertex from Tset if the indegree == outdegree
			#TODO: this should imporve. this should be submental instead of call getTSet directly
			#for vex in [outvex, invex]:
			#	if vex.indegree == vex.outdegree :
			#		#print("remove " + vex.name)
			#		Tset.remove(vex)
			Tset = self.getTSet()
	def getEurlerCircuit(self):
		ret = []
		#select start
		start = self.getStartVex()[0]
		#print "*****selected " + start.name + " as start "
		#select edge
		while 1:
			#select the edge
			for end in start.successor:
				edge = self.getEdge(start.name, end, 0)
				if not edge is None:
					break
			#return if no edge match
			if edge is None:
				return ret
			#mark as hitted
			edge.hit()
			#pprint("select edge: " + edge.start + ":" + edge.end)
			ret.append(edge)
			#pprint(vars(edge))
			start = self.getVertex(edge.end)
			#print "*****selected " + start.name + " as start "
	def getPathSet(self, circuit):
		ret = []
		curset = []
		for edge in circuit:
			#if is a fake, ignore it
			if edge.status == 1 and len(curset) != 0:
				self.fixPath(curset)
				ret.append(curset)
				curset = []
			#if is a normal edge add to the curset
			if edge.status == 0:
				curset.append(edge)
		return ret


	def getShortestPath(self, start, end):
		return []
	#if the start vex is not start type, should fix a path on the head 
	#if the end vex is not end type, should append a tail path
	def fixPath(self,path):
		#if it is not a start vex
		start = self.getVertex(path[0].start)
		end = self.getVertex(path[-1].end)
		head = []
		tail = []
		if start.postype & 1 != 0:
			head = self.getShortestPath(self.getStartVex()[0].name, start.name)
		if end.postype & 2 != 0:
			tail = self.getShortestPath(end.name, self.getEndVex()[1].name)
		return head + path + tail

	
		

#this is a test
if __name__ =='__main__':
	edge1 = Edge("A","B")
	edge2 = Edge("A","C")
	edge3 = Edge("B","D")
	edge4 = Edge("C","D")
	edge5 = Edge("B","C")
	g = Graph()
	g.addEdge(edge1)
	g.addEdge(edge2)
	g.addEdge(edge3)
	g.addEdge(edge4)
	g.addEdge(edge5)

	g.setVexPtype("A",1)
	g.setVexPtype("B",2)
	g.setVexPtype("C",2)
	g.setVexPtype("D",2)

	g.eulerize()
	#g.dump()
	edges = g.getEurlerCircuit()
	#for edge in edges:
	#	pprint(vars(edge))
	
	pathset = g.getPathSet(edges)
	for path in pathset:
		print "**********"
		for vex in path:
			vex.dump()

