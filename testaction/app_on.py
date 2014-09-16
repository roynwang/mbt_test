class app_on(object):
	def __init__(self):
		self.name = 'app_on'
	def transfer(self,status):
		if status['app'] != 'na' and status['black']!='on':
			status['app'] = 'on'
		return status

	def execute(self):
		print self.name
		return True
