from myraid.parser import Parser
#from myraid.compiler import Compiler
from myraid.memory.memory import Stack
#from rpython.rlib import rstring
import sys
import os
import re
class Main():
	def run(self, filename, name):
		codes = [];
		while True:
			read = os.read(filename, 4096);
			if len(read) == 0:
				break
			codes += read
		os.close(filename)
		contents = ""
		for line in codes:
			contents  = contents + line;
		codes = contents;
		codes = codes.split("\n");
		_codes = [];
		for function in codes:
			if function:
				_codes.append(function);
		print _codes;		
		i = 0;
		Psr = Parser()
		Psr.parse(_codes);

def entry_point(argv):
    try:
        filename = argv[1]
    except IndexError:
        print "You must supply a filename"
        return 1
    try:
        main = Main()
        main.run(os.open(filename, os.O_RDONLY, 0777), filename)
    except OSError:
        print "Could not open file. Reason: Non existent file"
    return 0

def target(*args):
    return entry_point, None;

if __name__ == "__main__":
    entry_point(sys.argv)
