from threading import Thread

class i(object):
	pass
i = i()
i.i = 0;

class Memory():
	def __init__(self):
		self.Collector = {}
	def Add(self, var_name, value):
		self.Collector[var_name] = value
	def Select(self, var_name):
		#print self.Collector
		return self.Collector[var_name];
		
class Stack():
	def __init__(self):
		self.stack = {}
	def Add(self, statement):
		i.i +=1
		self.stack[i.i] = statement
	def Select(self, x):
		return self.stack[x]
	def stmts(self):
		stack_ = {};
		i = 0;
		for stmt in self.stack:
			i+=1
			stack_[i] = self.stack[i]
		return stack_
		
class Sockets():
	def __init__(self):
		self.Socket_list = {}
	def Add(self, name, socket_data):
		self.Socket_list[name] = socket_data
	def Select(self, name):
		return self.Socket_list[name]
