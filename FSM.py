from Edge import *
from Action import *
import copy

class FSM(object):
	def __init__(self):
		self.name = "go"
		self.actionset = []
		self.startstates = []
		self.pathset = []

	def exploreSingle(self, state):
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
				edge = Edge(state,newsta, 0, action.name)

				#add to edge set if it's new
				
				if not edge in edgset:
					edgset.append(edge)

				#add to midstatus set if it's a new state
				if not newsta in tracked and not newsta in midstates:
					midstates.append(newsta)
			print "====================" + str(len(midstates))
			untracked = midstates
		return edgset
	
	def explore(self):
		for start in self.startstates:
			self.pathset += self.exploreSingle(start)
		self.pathset = list(set(self.pathset))
		return self.pathset


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
	fsm.explore()
	for edge in fsm.pathset:
		print(str(edge))
