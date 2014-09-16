class app_in(object):
	def __init__(self):
		self.name = 'app_in'
	def transfer(self,status):
		if status['black'] != 'on':
			status['app'] = 'on'
		return status
