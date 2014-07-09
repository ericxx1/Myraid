#make these functions except lists and turn the list values to what it needs. Example: name = list[0]; host = list[1]; port = list[2];
from rpython.rlib import rsocket
from rpython.rlib.rsocket import *
import os
import myraid_print
from myraid.memory import memory

#stack = Parser.stack

def eval(x, y, z):
	if y == "<":
		return x < z
	elif y == ">":
		return x > z
	elif y == ">=":
		return x >= z
	elif y == "<=":
		return x <= z
	elif y == "==":
		return x == z
	else:
		assert False, "Unknown comparison operator: %s" % y
def IF(args):
	x = args[0]
	y = args[1]
	z = args[2]
	if x.find('"') != -1:
		x = x
	elif(x.isdigit()):
		x = x
	else:
		x = mem.Select(x)
	if z.find('"') != -1:
		z =z 
	elif(z.isdigit()):
		z = z
	else:
		z = mem.Select(z)
	ev = eval(x, y, z)
	if str(ev) == "1":
		print "True"
	else:
		print "False"
	#return eval(str(x) + str(conditional) + str(y))
def ELSE(self):
	print "True"
	return None;
"""
def WHILE(a=1, b=">", c=0):
	if(a is True):
		return True;
	if(a is not True or a is not False):
		return eval(str(a) + str(b) + str(c))
	else:
		return False;
"""
global sockets
sockets = memory.Sockets();

global mem
mem = memory.Memory()
def INT():
	return None; #Add a math module for support for mathematical calculations via this recrusive math statement defined below.
def VAR(args): #Add addition subtraction etc support. Create a recursive statement such as the conditional statement to do such a thing. or perhaps just use the conditional statement for it. 
	print args
	try:
		var_name = args[0]
		value = args[1]
		print "Var name: " + var_name
		if '"' in value: #FIX DIS
			print "Added Variable"
			mem.Add(var_name, value)
		elif value.isdigit():
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
		myraid_socket = RSocket(AF_INET, SOCK_STREAM);
		sockets.Add(name, myraid_socket);
		print "Socket " + name + "created " + str(sockets.Select(name));
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
		print name
		print "Name:" + name + "," + host + "," + port
		myraid_socket = sockets.Select(name);
		#myraid_socket = sockets.Socket_list[name]
		try:
			addr = INETAddress(host, int(port))
			myraid_socket.connect(addr)
			print "Connected to " + host;
		except(rsocket.SocketError):
			print "Could not connect to " + host;
			pass	
	except Exception as e:
		ERROR(e)
	return None;
def CREATE_SOCKET_SERVER(args):
	return None;
def SEND_TO_SOCKET(args):
	try:
		name = args[0]
		to_send = args[1]
		myraid_socket = sockets.Select(name);
		myraid_socket.send(to_send.strip('"'));
	except Exception as e:
		ERROR(e)
	return None;
def SOCKET_RECV():
	myraid_socket.socket_recv(named, bytes_per_chunk)
	return None;
def _OSEXEC():
	return None;
