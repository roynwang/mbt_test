class Action(object):
	def __init__(self):
		self.name = 'test'
	
	def check(self):
		raise NotImplementedError()

	#it should return a status
	def transfer(self,status):
		raise NotImplementedError()

	def execute(self):
		raise NotImplementedError()

	def __str__(self):
		return str(self.name)
