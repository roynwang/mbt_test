from Edge import *
from Action import *
from Graph import *
import copy

class FSM(object):
	def __init__(self):
		self.name = "go"
		self.actionset = []
		self.startstates = []
		self.edgeset = []
		self.cases = []

	def generateEdgeByState(self, state):
		untracked = [state]
		tracked = []
		edgset = [] 
		while(len(untracked) > 0):
			midstates = []
			state = untracked.pop()
			tracked.append(state)
			for action in self.actionset:
				#get new status
				newsta = action.transfer(copy.deepcopy(state))
				#get new edge
				edge = Edge(state,newsta, 0, action)

				#add to edge set if it's new
				
				if not edge in edgset:
					edgset.append(edge)

				#add to midstatus set if it's a new state
				if not newsta in tracked and not newsta in midstates:
					midstates.append(newsta)
			untracked = midstates
		return edgset
	
	def generateEdge(self):
		#generate all edges
		for start in self.startstates:
			self.edgeset += self.generateEdgeByState(start)
		self.edgeset = list(set(self.edgeset))

	def explore(self):
		self.g = Graph()

		#generate all edges
		self.generateEdge()
		#add all edges in graph
		self.g.addEdge(self.edgeset)
		#set start states 
		self.g.setVexPtype(self.startstates, 1)

		self.g.eulerize()
		edges = self.g.getEurlerCircuit()
		'''
		print "===========Eu=========="
		self.g.outputpath(edges)
		print "===========End========="
		'''
		self.cases = self.g.getPathSet(edges)
	def execute_one(self, case):
		for edge in case:
			print "executing " + edge.action.name + " ... ..."
			if not edge.action.execute():
				return False
		return True
	def execute(self):
		for case in self.cases:
			print "=============Execution================"
			result = self.execute_one(case)
			print("================%s=================" % str(result) )
		
	def dumpcase(self):
		i = 0
		for case in self.cases:
			print("Case " + str(i) + ": " ),
			self.g.outputpath(case)
			i+=1

if __name__ == '__main__':
	fsm = FSM()
	action1 = Action()
	action1.transfer = lambda x : (x == "1" and "1" ) or "2"
	action1.name = "rule 1"
	action2 = Action()
	action2.transfer = lambda x : (x == "2" and "1") or "2"
	action2.name = "rule 2"
	fsm.actionset.append(action1)
	fsm.actionset.append(action2)
	fsm.startstates = ["1"]
	fsm.generateEdge()
	for edge in fsm.edgeset:
		print(str(edge))
