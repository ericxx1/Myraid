#make these functions except lists and turn the list values to what it needs. Example: name = list[0]; host = list[1]; port = list[2];
import os
import myraid_socket
import myraid_print
from myraid.memory import memory
#stack = Parser.stack
"""
def IF(x, conditional, y):
	return eval(str(x) + str(conditional) + str(y))
def ELSE_IF(x, conditional, y):
	return eval(str(x) + str(conditional) + str(y))
def ELSE():
	return True;
def WHILE(a=1, b=">", c=0):
	if(a is True):
		return True;
	if(a is not True or a is not False):
		return eval(str(a) + str(b) + str(c))
	else:
		return False;
"""
global mem
mem = memory.Memory()
def INT():
	return None;
def VAR(args):
	print args
	try:
		var_name = args[0]
		value = args[1]
		print "Var name: " + var_name
		if '"' in value: #FIX DIS
			print "Added Variable"
			mem.Add(var_name, value)
		else:
			value = mem.Select(value)
			value = value.strip('"')
			mem.Add(var_name, value)
			print "Added Variable"
			print value
	except Exception as e:
		ERROR(e)
	return None;
def FLOAT():
	return None;
def IN():				
	return None;
def LOAD():
	return None;
def CREATE_SOCKET(args):
	try:
		name = args[0]
		myraid_socket.create_socket(name)
	except Exception as e:
		ERROR(e)
	return None;
def ERROR(r):
	print r
	os._exit(0)
	return None;
def CONNECT_SOCKET(args):
	try:
		name = args[0]
		host = args[1]
		port = args[2]
		myraid_socket.connect_socket(name, host, port)
	except Exception as e:
		ERROR(e)
	return None;
def CREATE_SOCKET_SERVER(args):
	return None;
def SEND_TO_SOCKET(args):
	try:
		name = args[0]
		to_send = args[1]
		myraid_socket.send_to_socket(name, to_send)
	except Exception as e:
		ERROR(e)
	return None;
def SOCKET_RECV():
	myraid_socket.socket_recv(named, bytes_per_chunk)
	return None;
def _OSEXEC():
	return None;
