
import ply.yacc as yacc

from Tokenizer import Tokenizer


class Parser:

    def p_program(self, p):
        p[0] = p[1]

    def p_statement_list(self, p):
        if len(p) == 2 :      
            p[0] = [p[1]]
        else :
            p[0] = p[1] + [p[2]]

    def p_statement(self, p):
        p[0] = p[1]

    def p_declaration_statement(self, p):
        p[0] = p[2]

    def p_declaration_list(self, p):
        if len(p) == 2 :
            p[0] = [p[1]] 
        else :      
            p[0] = p[1] + [p[3]]


