class app_off(object):
	def __init__(self):
		self.name = 'app_off'

	def transfer(self,status):
		if status['app'] != 'na':
			status['app'] = 'off'
		return status
