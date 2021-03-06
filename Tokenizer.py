import ply.lex as lex

class Tokenizer:

    reserved = {
        "array": "ARRAY",
        "by": "BY",
        "chars": "CHARS",
        "dcl": "DCL",
        "do": "DO",
        "down": "DOWN",
        "else": "ELSE",
        "elsif": "ELSIF",
        "end": "END",
        "exit": "EXIT",
        "fi": "FI",
        "for": "FOR",
        "if": "IF",
        "in": "IN",
        "loc": "LOC",
        "od": "OD",
        "proc": "PROC",
        "ref": "REF",
        "result": "RESULT",
        "return": "RETURN",
        "returns": "RETURNS",
        "syn": "SYN",
        "then": "THEN",
        "type": "TYPE",
        "to": "TO",
        "while": "WHILE",
        "abs": "ABS",
        "asc": "ASC",
        "bool": "BOOL",
        "char": "CHAR",
        "false": "FALSE",
        "int": "INT",
        "length": "LENGTH",
        "lower": "LOWER",
        "null": "NULL",
        "num": "NUM",
        "print": "PRINT",
        "read": "READ",
        "true": "TRUE",
        "upper": "UPPER"
    }

    tokens = [
                 'ICONST',
                 'CCONST',
                 'SCONST',
                 'COMMA',
                 'PLUS',
                 'MINUS',
                 'TIMES',
                 'DIVIDE',
                 'COLON',
                 'LPAREN',
                 'RPAREN',
                 'ASSIGN',
                 'SEMI',
                 'ARROW',
                 'LTEQUAL',
                 'LESS',
                 'GREATER',
                 'GTEQUAL',
                 'EQUAL',
                 'LBRACKET',
                 'RBRACKET',
                 'ID',
                 'MODULO',
                 'AND',
                 'OR',
                 'NOTEQ',
                 'NOT',
                 'CONCAT',
                 'HAT'
             ] + list(reserved.values())

    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ASSIGN = r'='
    t_SEMI = r';'
    t_COLON = r':'
    t_ARROW = r'->'
    t_LBRACKET = r'\['
    t_RBRACKET = r'\]'
    t_COMMA = r','
    t_LTEQUAL = r'<='
    t_GTEQUAL = r'>='
    t_LESS = r'<'
    t_GREATER = r'>'
    t_EQUAL = r'=='
    t_MODULO = r'%'
    t_AND = r'&&'
    t_OR = r'\|\|'
    t_NOT = r'!'
    t_NOTEQ = r'!='
    t_CONCAT = r'&'
    t_HAT = r'\^'

    # Build the lexer
    
    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def t_ID(self, t):
        r'[a-zA-Z_][a-zA-Z_0-9]*'
        t.type = self.reserved.get(t.value, 'ID')  # Check for reserved words
        return t

    def tokenize(self, input):
        self.build()
        self.lexer.input(input)
        self.lexer.open_quote = 0
        self.lexer.open_comment = 0
        for tok in iter(lex.token, None):
            print (repr(tok.type), repr(tok.value))

    # Line, Tab, Spaces

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)


    t_ignore = ' \t'  
    
    # C and C++ comment style

    def t_COMMENT(self, t):
        r'(/\*(.|\n)*?\*/)|(//.*)'
        t.lexer.lineno += t.value.count('\n')
        pass

    def t_ICONST(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    # C string "string"

    def t_SCONST(self, t):
        r'\"(\\.|[^"])*\"'
        value = t.value[1:-1]
        value = value.replace('\\n', '\n')
        value = value.replace('\\t', '\t')
        t.value = value
        return t

    # C character literal 'char'
    def t_CCONST(self, t):
        r'\'(\\.|[^\'])*\'|\^\(\d*\)'
        if t.value[0] == "'":
            value = t.value[1:-1]
            value = value.replace('\\n', '\n')
            value = value.replace('\\t', '\t')
            value = ord(value)
        else:
            value = int(t.value[2:-1])
        t.value = value
        return t

    # Errors

    def t_error_unclosed_string(self, t):
        r'".*'
        print("%d: Unterminated string" % t.lexer.lineno)
        t.lexer.skip(1)


    def t_error_unclosed_comment(self, t):
        r'/\*.*'
        print("%d: Unterminated comment" % t.lexer.lineno)
        t.lexer.skip(1)


    def t_error(self, t):
        r'\\.*'
        print("%d: Bad string escape code '\%s'" % (t.lexer.lineno, t.value[1]))
        t.lexer.skip(1)
        
