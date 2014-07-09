from rply import ParserGenerator, LexerGenerator, ParsingError, token
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
	@pg.production("main : conditional")
	@pg.production("main : conditionals")
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
	
	@pg.production("conditional : ATOM CONDITIONAL ATOM")
	@pg.production("conditional : ATOM CONDITIONAL NUMBER")
	@pg.production("conditional : NUMBER CONDITIONAL ATOM")
	@pg.production("conditional : NUMBER CONDITIONAL NUMBER")
	def conditional(p):
		for value in p:
			value = value.getstr()
			print value
		return Boxes.BoxArray(p);
	
	@pg.production("conditionals : conditional")
	def conditionals(p):
		print "Single conditional"
		conditional = p[0]
		assert isinstance(conditional, Boxes.BoxArray)
		p = Boxes.BoxArray.getArray(conditional)
		p_ = []
		print p
		return Boxes.BoxArray(p);
					
	@pg.production("conditionals : conditionals CONDITIONAL conditional")
	def conditionals(p):
		print "Conditionals CONDITIONAL conditional"
		print p
		p_ = []
		conditional1 = p[0]
		conditional2 = p[2]
		condition = p[1]
		assert isinstance(conditional1, Boxes.BoxArray)
		conditional1 = Boxes.BoxArray.getArray(conditional1)
		for value in conditional1:
			p_.append(value)
		p_.append(condition)
		assert isinstance(conditional2, Boxes.BoxArray)
		conditional2 = Boxes.BoxArray.getArray(conditional2)
		for value in conditional2:
			p_.append(value)
		print p_
		return Boxes.BoxArray(p_);
	
	#Add if( x in y ) or just x in y: without if. Add support for strings. String in x etc.
	#Statements
	@pg.production("conditionals : IF conditional")
	@pg.production("conditionals : IF OPEN_PAREN conditional CLOSED_PAREN")
	@pg.production("conditionals : IF OPEN_PAREN conditionals CLOSED_PAREN")
	@pg.production("conditionals : ELSEIF OPEN_PAREN conditionals CLOSED_PAREN")
	@pg.production("conditionals : IF conditionals")
	@pg.production("conditionals : ELSEIF conditionals")
	def if_op(p):
		print "if statement"
		if p[1].getstr() == "(":
			conditions = p[2]
			assert isinstance(conditions, Boxes.BoxArray)
			conditions = Boxes.BoxArray.getArray(conditions)
			statement = ""
			for value in conditions:
				value = value.getstr()
				statement += value+","
			statement = statement[:-1]
			op = p[0].getstr().upper() + "(" + statement + ")"
			stack.Add(op);
		else:
			conditions = p[1]
			assert isinstance(conditions, Boxes.BoxArray)
			conditions = Boxes.BoxArray.getArray(conditions)
			statement = ""
			for value in conditions:
				value = value.getstr()
				statement += value+","
			statement = statement[:-1]
			op = p[0].getstr().upper() + "(" + statement + ")"
		stack.Add(op);
		return None;
		
	@pg.production("string : ELSE")
	def else_op(p):
		print "else op"
		stack.Add("ELSE")
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
