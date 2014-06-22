from myraid.memory import memory
from rpython.rlib.rsocket import *
import sys

def entry_point(argv):
	mem = memory.Memory()
	sk = memory.Stack()
	sock = memory.Sockets()
	x = "hi"
	y = "dong"
	mem.Add(x, y)
	mem.Add("shit", "head")
	print mem.Select(x)
	print mem.Select("shit")
	sk.Add("big dick")
	print sk.Select(1)
	myraid_socket = RSocket(AF_INET, SOCK_STREAM);
	myraid_socket_ = RSocket(AF_INET, SOCK_STREAM);
	sock.Add("Test", myraid_socket)
	sock.Add("Test1", myraid_socket_)
	print sock.Select("Test")
	print sock.Select("Test1")
	return 0

def target(*args):
	return entry_point, None;

if __name__ == "__main__":
    entry_point(sys.argv)
