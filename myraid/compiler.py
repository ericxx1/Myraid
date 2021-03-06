from functions import myraid_functions
from rpython.rlib import rstring #Imports rPython rString
class Compiler():
	global lookup_table
	lookup_table = {
	"CREATE_SOCKET" : myraid_functions.CREATE_SOCKET, #Ask simpson how to make it so it only asks for args upon execution like in his example;
	"SOCKET_CONNECT" : myraid_functions.CONNECT_SOCKET,
	"CREATE_SOCKET_SERVER" : myraid_functions.CREATE_SOCKET_SERVER,
	"SOCKET_SEND" : myraid_functions.SEND_TO_SOCKET,
	"VAR" : myraid_functions.VAR,
	"IF": myraid_functions.IF,
	"ELSEIF": myraid_functions.IF,
	"ELSE": myraid_functions.ELSE
	}
	def splitter(statement):
		values = [];
		_values = [];
		p = 0;
		m = False;
		if("," in statement):
			values = rstring.split(statement, ",")
			#values = statement.split(","); #strip the ( and )
			m = True;
		#for value in values:
		#	print value
		if(m == True):
			for value in values:
				p+=1;
				if value.find("(") != -1:
					if value == values[0]:
						f1 = value
						f0, f1 = rstring.split(f1, "(")
						f1 = f1.strip(")")
						#_values.append(f0)
						_values.append(f1)
				else:
					_values.append(value.strip(")"))
				#elif value.startswith("("):
				#	value = value[1:]
				#	_values.append(value);
				#
				#elif value.endswith(")"):
				#	value = value[:-1]
				#	_values.append(value);
				#else:
				#	_values.append(value)
		else:
			f1 = statement
			if "(" in f1:
				f0, f1 = rstring.split(f1, "(")
				f1 = f1.strip(")")
			#_values.append(f0)
			_values.append(f1)
		return _values

	def compile(self, stack):
		i = 0;
		y = 0;
		print "Compiling..."
		for value in stack:
			y+=1;
			print stack[y]
		for statement in stack:
			i+=1;
			statement = str(stack[i])
			print statement
			if("(" in statement):
				atoms = statement.split("(")
				keyword = atoms[0]
			else:
				keyword = str(statement);
			d = Compiler.splitter(statement);
			print keyword
			for value in d:
				print value
			lookup_table[keyword](d); #Somehow pass a list to all functions that need more than 1 values. Pass list, assign x,y,z from list[0] list[1] list[2] or something
		return None;
