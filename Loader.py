import imp
import pprint
import os

class Loader(object):

	ATTRS = ["transfer", "execute"]
	def __init__(self, path):
		self.path = path
		self.mods = []
		self.actions = []
	def load_from_file(self,filepath):
		py_mod = None
		mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

		if file_ext.lower().endswith('.py'):
			py_mod = imp.load_source(mod_name, filepath)	
		else:
			return None
		'''
		#ignore the pyc file
		elif file_ext.lower() == '.pyc':
			py_mod = imp.load_compiled(mod_name, filepath)
		'''
		cls = None
		if hasattr(py_mod,mod_name):
			cls = getattr(py_mod,mod_name)
			if Loader._isaction(cls):
				print("loaded action :" +  filepath)
				return cls
		else:
			exec("from " + mod_name + " import *")
			print("imported module :" +  filepath)
		return None

	def load(self):
		if os.path.isfile(self.path):
			self.mods.append(self.load_from_file(self.path))
		elif os.path.isdir(self.path):
			files = [ os.path.join(self.path,f) for f in os.listdir(self.path) if f.endswith('.py') and os.path.isfile(os.path.join(self.path,f)) ]
			for f in files:
				mod =self.load_from_file(f)
				if not mod is None:
					self.mods.append(mod)
		self.createInstance()
	@staticmethod
	def _isaction(obj):
		for attr in Loader.ATTRS:
			if not hasattr(obj, attr):
				return False
		return True

	def createInstance(self):
		for mod in self.mods:
			obj = mod()
			self.actions.append(obj)

	def __str__(self):
		ret = ''
		for mod in self.mods:
			ret += str(mod)
			ret +=';\n'
		for action in self.actions:
			ret += str(action)
			ret +=';\n'
		return ret

if __name__ == "__main__":
	loader = Loader("./testaction")
	loader.load()
	print str(loader)




