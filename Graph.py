from Edge import *
from Vertex import *
import json
from pprint import pprint
import uuid
from Drawer import *

class Graph(object):
	def __init__(self):
		self.vertexes = []
		self.edges = []
		self.degreedict = {}
	def addEdge(self, edges):
		if isinstance(edges, Edge):
			edges = [edges]

		for edge in edges:
			if not edge in self.edges:
				self.edges.append(edge)
				self.updateVertex(edge)
	def updateVertex(self, edge):
		# add the vertex
		start = edge.start
		end = edge.end
		if len(self.vertexes) == 0 or not start in self.vertexes:
			self.vertexes.append(start)
		if len(self.vertexes) == 0 or not end in self.vertexes:
			self.vertexes.append(end)
		vert = self.getVertex(edge.start)
		#update the adjacency and degree
		#the in-degree of end will increment too
		vert.addSuccessor(self.getVertex(edge.end))

	def outputpath(self, pathset):
		start = True
		for path in pathset:
			if start:
					print str(path.start),
					start = False
			print "=>|" +str(path.action) + "|",
			print "=>" + str(path.end),
		print("")

	def getVertex(self, vex):
		eq = None
		if isinstance(vex, basestring) :
			#print "vex is str"
			eq = lambda x,y: x == y.name
		else:
			#print "vex is obj"
			eq = lambda x,y:  str(x) == str(y)
		for vert in self.vertexes:
			if eq(vex, vert):
				return vert
		return None
	def setVexPtype(self, names, ptype):
		if not isinstance(names, list):
			names = [names]
		for name in names:
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
			print str(edge)
		print("================")
		for ver in self.vertexes:
			print str(ver)


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
				if vex.indegree<vex.outdegree and not outvex.isSuccessor(vex):
					invex = vex
					break

			#create a fake vertex if there is no proper choice
			fake = None
			if outvex is None:
				fake = outvex = Vertex(str(uuid.uuid1()), 1)
			elif invex is None:
				fake = invex = Vertex(str(uuid.uuid1()), 1)

			#create a fake edge: outvex=>invex
			print("add fake edge from " + str(outvex) + " to " +  str(invex))
			self.addEdge(Edge(outvex, invex, 1))

			#update fake status: SHOULD mark it as a fake vertex
			if not fake is None:
				fake.status = 1
				Tset.append(fake)

			#remove the vertex from Tset if the indegree == outdegree
			for vex in [outvex, invex]:
				if vex.indegree == vex.outdegree :
					Tset.remove(vex)
	def refreshVertexes(self):
		ordered = []
		for edge in self.edges:
			if not edge.start in ordered :
				ordered.append(edge.start)
			if not edge.end in ordered :
				ordered.append(edge.end)
		self.vertexes = ordered

	def getEurlerCircuit(self):
		ret = []
		ordered = []
		#select start
		start = self.getStartVex()[0]

		#print "*****selected " + start.name + " as start "
		#select edge
		while 1:
			#select the edge
			edge = None
			for end in start.successor:
				edge = self.getEdge(start, end, 0)
				if not edge is None:
					break
			#return if no edge match
			if edge is None:
				self.edges = ret
				self.refreshVertexes()
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
				curset = self.fixPath(curset)
				ret.append(curset)
#				self.outputpath(curset)
				curset = []
			#if is a normal edge add to the curset
			if edge.status == 0:
				curset.append(edge)
		return ret

	def getShortestPath(self, start, end, visited = []):
		tmp = []
		#this is too avoid cycle, search will stop if the path length > vex count
		size = len(self.vertexes)
		if start == end:
			return [start]
		isfaked = lambda g,s,e: g.getEdge(s,e).isFaked()
		for suc in start.successor:
			if not suc in visited and not isfaked(self, start, suc):
				subset = self.getShortestPath(suc, end, visited+[start])
				if len(subset) < size and len(subset) > 0 :
					tmp = [start] + subset
		return tmp

	def convertVexesToPaths(self, vexes):
		paths = []
		for i in range(1,len(vexes)):
			paths.append(self.getEdge(vexes[i-1], vexes[i]))
		return paths

	#if the start vex is not start type, should fix a path on the head 
	#if the end vex is not end type, should append a tail path
	def fixPath(self,path):
		#if it is not a start vex
		start = self.getVertex(path[0].start)
		end = self.getVertex(path[-1].end)
		head = []
		tail = []
		if start.postype & 1 == 0:
			#print "get shortest " + self.getStartVex()[0].name + "=>" + start.name
			head = self.getShortestPath(self.getStartVex()[0], start)
			head = self.convertVexesToPaths(head)
#			self.outputpath(head)
		if end.postype & 2 == 0:
			#print "shortest " + end.name + "=>" + self.getEndVex()[0].name
			tail = self.getShortestPath(end, self.getEndVex()[0])
			tail = self.convertVexesToPaths(tail)
#		self.outputpath(head + path + tail)
		return head + path + tail
	def savesvg(self):
		drawer = Drawer(self)
		drawer.gen()
		print "save as svg file"
		drawer.save()


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

	#1 mean the start state
	#2 mean the end state
	g.setVexPtype("A",1)
	#g.setVexPtype("B",2)
	#g.setVexPtype("C",2)
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
			print(str(vex))
	g.savesvg()

