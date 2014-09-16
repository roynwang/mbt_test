import imp
import pprint
import os

class Loader(object):
	def __init__(self, path):
			self.path = path
			self.mods = []
			self.actions = []
	def load_from_file(self,filepath):
		print("loading " +  filepath)
		py_mod = None
		mod_name, file_ext = os.path.splitext(os.path.split(filepath)[-1])

		if file_ext.lower().endswith('.py'):
			py_mod = imp.load_source(mod_name, filepath)	
		else:
			return None
		#ignore the pyc file
#		elif file_ext.lower() == '.pyc':
#			py_mod = imp.load_compiled(mod_name, filepath)
		
		return getattr(py_mod,mod_name)

	def load(self):
		if os.path.isfile(self.path):
			self.mods.append(self.load_from_file(self.path))
		elif os.path.isdir(self.path):
			files = [ os.path.join(self.path,f) for f in os.listdir(self.path) if f.endswith('.py') and os.path.isfile(os.path.join(self.path,f)) ]
			for file in files:
				self.mods.append(self.load_from_file(file))

	def createInstance(self):
		for mod in self.mods:
			self.actions.append(mod())

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
	loader.createInstance()
	print str(loader)
	

		
	
