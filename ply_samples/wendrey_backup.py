def p_program(self, p):
    " <program> ::= { <statement> }+ "
    p[0] = p[1]


def p_statement_list(self, p):
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + [p[2]]


def p_statement(self, p):
    " <statement> ::= <declaration_statement> | <synonym_statement> | <newmode_statement> | <procedure_statement> | <action_statement> "
    p[0] = p[1]


# Declaration Statement

def p_declaration_statement(self, p):
    " <declaration_statement> ::= DCL <declaration_list> ; "
    p[0] = p[2]


def p_declaration_list(self, p):
    " <declaration_list> ::= <declaration> { , <declaration> }* "
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_declaration(self, p):
    " <declaration> ::= <identifier_list> <mode> [ <initialization> ] "
    if len(p) == 3:
        p[0] = p[1] + p[2]
    else:
        p[0] = p[1] + p[2] + p[3]


def p_initialization(self, p):
    " <initialization> ::=  <assignment_symbol> <expression> "
    p[0] = p[1] + p[2]


def p_identifier_list(self, p):
    " <identifier_list> ::= <identifier> { , <identifier> }* "
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_identifier(self, p):
    " <identifier> ::= [a-zA-Z_][a-zA-Z_0-9]* "
    p[0] = p[1]


# Synonym Statement

def p_synonym_statement(self, p):
    " <synonym_statement> ::= SYN <synonym_list> ; "
    p[0] = p[2];


def p_synonym_list(self, p):
    " <synonym_list> ::= <synonym_definition> { , <synonym_definition> }* "
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]


def p_synonym_definition(self, p):
    " <synonym_definition> ::= <identifier_list> [ <mode> ] = <constant_expression> "
    if len(p) == 4:
        p[0] = p[1] + p[3]
    else:
        p[0] = p[1] + p[2] + p[4]


def p_constant_expression(self, p):
    " <constante_expression> ::= <expression> "
    p[0] = p[1]
