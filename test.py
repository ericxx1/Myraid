from threading import Thread
class i(object):
	pass
i = i()
i.i = 0;
class Stack(Thread):
	def __init__(self):
		self.stack = {}
	def Add(self, statement):
		i.i +=1
		self.stack[i.i] = statement
	def Select(self, x):
		return self.stack[x]
	def stmts(self):
		stack = {};
		i = 0;
		for stmt in self.stack:
			i+=1
			stack[i] = self.stack[i]
		return stack
		
class Memory(Thread):
	def __init__(self):
		self.Collector = {}
	def Add(self, var_name, value):
		self.Collector[var_name] = value
	def Select(self, var_name):
		print self.Collector
		return self.Collector[var_name];
		
def VAR(*args):
	print args
	var_name = args[0]
	value = args[1]
	if not value.find('"') != -1:
		print "Var name: " + var_name
		print mem.Select(value)
		value = mem.Select(value)
	mem.Add(var_name, value)
mem = Memory()
mem.Add("dick", "dong")
VAR("d", "dick")
VAR("p", "d")
print mem.Select("p")
