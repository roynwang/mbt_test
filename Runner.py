from Loader import *
from FSM import *

class Runner(object):
	def __init__(self, path, startstates=[]):
		self.path = path
		self.fsm = FSM()
		self.loader = Loader(path)
		self.startstates = startstates
	def prepare(self):
		self.loader.load()
		self.fsm.startstates = self.startstates
		self.fsm.actionset = self.loader.actions
		self.fsm.explore()
	def run(self):
		self.fsm.execute()

if __name__ == '__main__':
	runner = Runner("./testaction",[{'app':'na', 'black':'na'}])
	runner.prepare()
	runner.run()
		
		
