class Vertex(object):
	#status:0 => normal 
	#status:1 => fake
	def __init__(self, name, status=0):
		self.name = name
		self.successor= []
		self.outdegree = 0
		self.indegree = 0
		self.status = status
		self.postype = 2

	def isFaked(self):
		return self.status == 1

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

	def __str__(self):
		return str(self.name)
