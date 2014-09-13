class Vertex(object):
	def __init__(self, name, status=0):
		self.name = name
		self.successor= []
		self.outdegree = 0
		self.indegree = 0
		self.status = status
		self.postype = 0

	def addSuccessor(self, succ):
		if len(self.successor) ==0 or not succ in self.successor:
			self.successor.append(succ)
			self.outdegree += 1
			succ.indegree += 1

	def setpostype(self, v):
		self.postype = v

	def isSuccessor(self,vex):
		return vex is None or vex in self.successor

	def __eq__(self, other):
		return self.name == other.name
