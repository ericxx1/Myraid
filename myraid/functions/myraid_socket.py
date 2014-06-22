from rpython.rlib import rsocket
from rpython.rlib.rsocket import *
from ..memory import memory

global sockets
sockets = memory.Sockets();

def create_socket(name):
	myraid_socket = RSocket(AF_INET, SOCK_STREAM);
	sockets.Add(name, myraid_socket);
	print "Socket created " + str(sockets.Select(name));
	
def connect_socket(name, host, port):
	print "Name:" + name + "," + host + "," + port
	#myraid_socket = sockets.Select(name);
	myraid_socket = sockets.Socket_list[name]
	try:
		addr = INETAddress(host, int(port))
		myraid_socket.connect(addr)
		print "Connected to " + host;
	except(rsocket.SocketError):
		print "Could not connect to " + host;
		pass
		
def create_socket_server(name, port):
	try:
		myraid_socket = sockets.Select(name);
		myraid_socket.bind(INETAddress('localhost', int(port)));
		print "Socket binded on port " + port
	except(rsocket.SocketError):
		return "Could not bind to port " + port;
		pass
		
def send_to_socket(name, data):
	myraid_socket = sockets.Select(name);
	myraid_socket.send(data);
	
def socket_recv(name, bytes_per_chunk):
	myraid_socket = sockets.Select(name);
	data = myraid_socket.recv(int(bytes_per_chunk));
	return data;
