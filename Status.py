


#it should contain a dict for status a check rule set
class Status(object):
	def __init__(self):
		self.status = {}
	def update(self,key, value):
		self.status[key] = value
	def check(self):
		raise NotImplementedError()
