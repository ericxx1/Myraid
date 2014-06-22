from rply import ParserGenerator, LexerGenerator, ParsingError
lg = LexerGenerator()
# Add takes a rule name, and a regular expression that defines the rule.
keywords = ["IF", "WHILE", "NEW", "SOCKET", "COLON", "NUMBER", "PLUS", "MINUS", "MULTIPLY",
           "DIVIDE", "NUMBER", "STRING", "OPEN_PAREN", "CLOSED_PAREN", "COMMA", "RECV",
           "SEND", "OBJECT", "VAR", "NAME", "CONDITIONAL", "PERIOD", "EQUAL", "COMMENT",
           "END", "GREATER_THAN_OR_EQUAL_TO", "LESS_THAN_OR_EQUAL_TO"]
operations = ["CONNECT"]
lg.add("PLUS", r"\+")
lg.add("MINUS", r"-")
lg.add("MULTIPLY", r"\*")
lg.add("DIVIDE", r"/")
lg.add("EQUAL", r"=")
lg.add("NUMBER", r"\d+")
lg.add("STRING", r'\"[\w\s\.]+\"')
lg.add("NEW", r"\New")
lg.add("SOCKET", r"\Socket")
lg.add("OPEN_PAREN", r"[(]")
lg.add("CLOSED_PAREN", r"[)]")
lg.add("COLON", r"\:")
lg.add("CONNECT", r"\connect")
lg.add("SEND", r"\Send")
lg.add("COMMA", r"\,")
lg.add("OBJECT", r"([A-Za-z0-9_\./\\-]*)\.")
lg.add("IF", r"\if")
lg.add("ELSEIF", r"\elseif")
lg.add("ELSE", r"\else")
lg.add("END", r"\end")
lg.add("PERIOD", "\.")
lg.add('QUOTE', '\"')
lg.add("CONDITIONAL", r"[^\w\s]+")
lg.add("GREATER_THAN_OR_EQUAL_TO", ">=")
lg.add("LESS_THAN_OR_EQUAL_TO", "<=")
lg.add("ATOM", r"[a-zA-Z]+")
lg.add("COMMENT", r"//(.*)//")
lg.add("IN", r"\in")
lg.add("PERIOD", r"\.")
lg.ignore(r"\s+")
lexer = lg.build()
