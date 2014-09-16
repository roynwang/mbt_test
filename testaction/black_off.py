class black_off(object):
	def __init__(self):
		self.name = 'black_off'

	def transfer(self, status):
		status['black'] = 'off'
		if status['app'] == 'off':
			status['app'] = 'on'
		return status
	def execute(self):
		print self.name
		return True
