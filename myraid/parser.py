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
	parser = pg.build()
	def parse(self, statements):
		for statement in statements:
			tokens = lexer.lexer.lex(statement)
			for token in tokens:
				print("TOKEN:('"+token.gettokentype()+"','"+token.getstr()+"')")
			self.parser.parse(lexer.lexer.lex(statement))
		cm = Compiler()
		cm.compile(stack.stack)			
