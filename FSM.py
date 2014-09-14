from Edge import *
from Action import *

class FSM(object):
	def __init__(self):
		self.name = "go"
		self.actionset = []
		self.startstates = []

	def run(self, state):
		untracked = [state]
		tracked = []
		edgset = [] 
		while(len(untracked) > 0):
			midstates = []
			state = untracked.pop()
			for action in self.actionset:
				#get new status
				newsta = action.transfer(state)
				#get new edge
				edge = Edge(state,newsta)
				#add to edge set if it's new
				if not edge in edgset:
					edgset.append(edge)
				#add to midstatus set if it's a new state
				if not newsta in tracked and not newsta in midstates:
					midstates.append(newsta)
			tracked.append(state)
			untracked = midstates
		return edgset


if __name__ == '__main__':
	fsm = FSM()
	action1 = Action()
	action1.transfer = lambda x : (x == "1" and "1" ) or "2"
	action2 = Action()
	action2.transfer = lambda x : (x == "2" and "1") or "2"
	fsm.actionset.append(action1)
	fsm.actionset.append(action2)
	edgeset = fsm.run("1")
	for edge in edgeset:
		edge.dump()
				

			

