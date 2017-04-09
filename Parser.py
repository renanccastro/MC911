import ply.yacc as yacc

from Tokenizer import Tokenizer
from nodes.AST import AST
from nodes.DeclarationStatement import DeclarationStatement
from nodes.Declaration import Declaration
from nodes.Program import Program
from nodes.Identifier import Identifier

class Parser:
    tokens = Tokenizer.tokens
    # Program and Statement
    def p_program(self, p):
        'program : statement_list'
        p[0] = Program(p[1])

    def p_statement_list(self,p):
        'statement_list : statement statement_nullable'
        if len(p) == 2:
            p[0] = [DeclarationStatement(p[1])]
        elif len(p) == 3:
            p[0] = p[1]
            if p[2] is not None:
                p[0] = p[0] + p[2]

    def p_statement_nullable(self, p):
        '''statement_nullable : statement statement_nullable
                              | empty'''
        if len(p) == 2 and p[1] is not None:
            p[0] = [DeclarationStatement(p[1])]
        elif len(p) == 3:
            p[0] = p[1]
            if p[2] is not None:
                p[0] = p[0] + p[2]
        else:
            pass

    def p_statement(self, p):
        '''statement : declaration_statement'''
        p[0] = p[1]


    def p_declaration_statement(self, p):
        'declaration_statement : DCL declaration_list SEMI'
        p[0] = [DeclarationStatement(p[2])]

    def p_declaration_list(self, p):
        '''declaration_list : declaration
                            | declaration COMMA declaration'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = p[1]
            p[0].append(p[3])


    #TODO: falta colocar a inicializacao da declaracao
    def p_declaration(self,p):
        '''declaration : identifier_list mode'''
        p[0] = Declaration(p[1],p[2])

    def p_identifier_list(self,p):
        '''identifier_list : ID
                           | ID COMMA identifier_list'''
        if len(p) == 2:
            p[0] = [Identifier(p[1])]
        elif len(p) > 3:
            p[0] = p[3]
            p[0].append(Identifier(p[1]))

    # def p_identifier_append(self,p):
    #     '''identifier_append : COMMA ID
    #                          | identifier_append COMMA ID
    #                          | empty'''
    #     if len(p) > 1:
    #         p[0] = Identifier(p[2])
    #     else:
    #         pass

    def p_mode(self,p):
        '''mode : discrete_mode'''
        p[0] = p[1]
    def p_discrete_mode(self,p):
        '''discrete_mode : integer_mode
                         | boolean_mode
                         | character_mode'''
        p[0] = p[1]

    def p_integer_mode(self,p):
        'integer_mode : INT'
        p[0] = p[1]
    def p_boolean_mode(self,p):
        'boolean_mode : BOOL'
        p[0] = p[1]
    def p_character_mode(self,p):
        'character_mode : CHAR'
        p[0] = p[1]

    # empty
    def p_empty(self, p):
        'empty :'
        pass
    # Error rule for syntax errors
    def p_error(self, error):
        print("Syntax error in input!")

    def build(self):
        self.parser = yacc.yacc(module=self)
