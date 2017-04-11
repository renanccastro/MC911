import ply.yacc as yacc

from Tokenizer import Tokenizer
from nodes.AST import AST
from nodes.DeclarationStatement import DeclarationStatement
from nodes.Declaration import Declaration
from nodes.DiscreteMode import IntegerMode, BooleanMode, CharMode, DiscreteModeName
from nodes.DiscreteRangeMode import DiscreteRangeMode
from nodes.ModeName import ModeName
from nodes.Program import Program
from nodes.Identifier import Identifier
from nodes.Range import Range
from nodes.ReferenceMode import ReferenceMode


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


    def p_mode(self,p):
        '''mode : mode_name
                | discrete_mode
                | reference_mode'''
        p[0] = p[1]


    # TODO: Ver se eh necessario criar uma AST para o modo
    def p_mode_name(self,p):
        '''mode_name : ID'''
        p[0] = ModeName(p[1])


    def p_discrete_mode(self,p):
        '''discrete_mode : integer_mode
                         | boolean_mode
                         | character_mode
                         | discrete_range_mode'''
        p[0] = p[1]

    def p_integer_mode(self,p):
        'integer_mode : INT'
        p[0] = IntegerMode()
    def p_boolean_mode(self,p):
        'boolean_mode : BOOL'
        p[0] = BooleanMode()
    def p_character_mode(self,p):
        'character_mode : CHAR'
        p[0] = CharMode()

    def p_discrete_range_mode(self,p):
        '''discrete_range_mode : discrete_mode_name  LPAREN literal_range RPAREN
                               | discrete_mode LPAREN literal_range RPAREN'''
        p[0] = DiscreteRangeMode(p[1],p[3])

    def p_literal_range(self,p):
        '''literal_range : lower_bound COLON upper_bound'''
        p[0] = Range(p[1],p[3])

    # TODO: AQUI DEVE SER UMA EXPRESSION, MAS AINDA TEM QUE FAZER
    def p_lower_bound(self,p):
        '''lower_bound : ICONST'''
        p[0] = p[1]
    def p_upper_bound(self, p):
        '''upper_bound : ICONST'''
        p[0] = p[1]



    def p_discrete_mode_name(self,p):
        '''discrete_mode_name : ID'''
        p[0] = DiscreteModeName(p[1])

    def p_reference_mode(self,p):
        '''reference_mode : REF mode'''
        p[0] = ReferenceMode(p[2])

    # empty
    def p_empty(self, p):
        'empty :'
        pass
    # Error rule for syntax errors
    def p_error(self, error):
        print("Syntax error in input!")

    def build(self):
        self.parser = yacc.yacc(module=self)
