from _commonfun import testfunction
class app_in(object):
	def __init__(self):
		self.name = 'app_in'
	def transfer(self,status):
		if status['black'] != 'on':
			status['app'] = 'on'
		return status
	def execute(self):
		testfunction()
		print self.name
		return True
