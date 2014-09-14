


#it should contain a dict for status a check rule set
class Status(object):
	def __init__(self):
		self.status = {}
	def check(self):
		raise NotImplementedError()
