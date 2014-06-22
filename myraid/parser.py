from rply import ParserGenerator, LexerGenerator, ParsingError
from myraid import lexer
from myraid.memory import memory
from myraid.BaseBox import Boxes
from myraid.compiler import Compiler
class Parser(object):
	pg = ParserGenerator(["NUMBER", "STRING", 'MULTIPLY', "PLUS", "MINUS", "DIVIDE", "NEW", "SOCKET", "OPEN_PAREN",
	                      "CLOSED_PAREN", "COLON", "COMMA", "CONNECT", "SEND", "OBJECT", "IF", "ELSEIF", "ELSE", "QUOTE",
	                      "CONDITIONAL", "EQUAL", "NAME", "ATOM", "COMMENT", "END", "GREATER_THAN_OR_EQUAL_TO", 
	                      "LESS_THAN_OR_EQUAL_TO", "IN", "PERIOD"],
	        precedence=[("left", ['PLUS', 'MINUS']), ("left", ['MULTIPLY', 'DIVIDE'])], cache_id="myparser")
	global stack
	stack = memory.Stack()
	@pg.production("main : string")
	@pg.production("main : expr")
	@pg.production("main : variable")
	def main(p):
	    # p is a list, of each of the pieces on the right hand side of the
	    # grammar rule
	    return p[0]
	    
	@pg.production("expr : NUMBER")
	def expr_num(p):
	    return Boxes.BoxInt(int(p[0].getstr()))
	@pg.production("string : STRING")
	def string_op(s):
		return Boxes.BoxStr(s[0])
	@pg.production("variable : ATOM")
	def var_op(p):
		return p[0];
	    
	@pg.production("variable : ATOM  ATOM  EQUAL  NUMBER")    
	@pg.production("variable : ATOM  ATOM  EQUAL  ATOM")
	@pg.production("variable : ATOM  ATOM  EQUAL  STRING")
	def var(p):
		var_name = str(p[1].getstr())
		value = p[3].getstr()
		op = "VAR(" + var_name + "," + value + ")"
		stack.Add(op)	
		return None;
		
	@pg.production("string : ATOM OPEN_PAREN CLOSED_PAREN")
	def function_op(p):
		if(p[0].getstr() == "dstack"):
			i = 0;
			for value in stack.stack:
				i+=1;
				print stack.stack[i];
		return None;		
		
	#Sockets
	@pg.production("string : NEW SOCKET OPEN_PAREN string CLOSED_PAREN COLON")  
	def socket_op(p):
		name = p[3]
		assert isinstance(name, Boxes.BoxStr);
		name = Boxes.BoxStr.get_str(name)
		name = name.getstr().strip('"')
		print name
		op = "CREATE_SOCKET(" + name + ")"
		stack.Add(op);
		return None;
	
	@pg.production("string : OBJECT CONNECT OPEN_PAREN string COMMA NUMBER CLOSED_PAREN")
	def socket_connect_op(p):
		name = p[0].getstr().strip('.')
		print name #<----Strip name of '"' and "."
		host = p[3]
		assert isinstance(host, Boxes.BoxStr);
		host = Boxes.BoxStr.get_str(host)
		host = host.getstr().strip('"')
		print host
		port = p[5].getstr()
		print port
		op = "SOCKET_CONNECT(" + name + "," + host + "," + port + ")"
		stack.Add(op);
		return None
	
	@pg.production("string : OBJECT SEND OPEN_PAREN string CLOSED_PAREN") #Change SEND to ATOM eventually
	def socket_send_op(p):
		name = p[0].getstr().strip(".")
		#assert isinstance(name, Boxes.BoxStr);
		#name = Boxes.BoxStr.get_str(name)
		#name = name.getstr().strip(".")
		if(p[1].getstr() == "send"):
			to_send = p[3] #Fix this. Key error for some reason
			assert isinstance(to_send, Boxes.BoxStr);
			to_send = Boxes.BoxStr.get_str(to_send)
			to_send = to_send.getstr().strip('"')
			op = "SOCKET_SEND(" + name + "," + '"' + to_send + '"' + ")"
			stack.Add(op);
		return None
	
	@pg.production("string : OBJECT ATOM OPEN_PAREN NUMBER CLOSED_PAREN")	#Fix not being able to name a socket "Socket/socket. Change the New Socket (SOCKET) token to just a ATOM and identify it as a "socket""
	def socket_recv_op(p):
		name = p[0].getstr().strip(".")
		bytes_per_chunk = p[3].getstr()	
		op = "SOCKET_RECV(" + name + "," + bytes_per_chunk + ")"
		stack.Add(op);
		return None;
		
	parser = pg.build()
	def parse(self, statements):
		for statement in statements:
			tokens = lexer.lexer.lex(statement)
			for token in tokens:
				print("TOKEN:('"+token.gettokentype()+"','"+token.getstr()+"')")
			self.parser.parse(lexer.lexer.lex(statement))
		cm = Compiler()
		cm.compile(stack.stack)			
