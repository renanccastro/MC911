import ply.yacc as yacc

from Tokenizer import Tokenizer
from nodes.NewModeStatement import NewModeStatement
from nodes.AST import AST
from nodes.DeclarationStatement import DeclarationStatement
from nodes.Declaration import Declaration
from nodes.DiscreteMode import IntegerMode, BooleanMode, CharMode, DiscreteModeName
from nodes.DiscreteRangeMode import DiscreteRangeMode
from nodes.Expression import Expression
from nodes.Literal import IntegerLiteral, BoolLiteral, CharLiteral, NullLiteral, StringLiteral
from nodes.ModeDefinition import ModeDefinition
from nodes.ModeName import ModeName
from nodes.Modes.CompositeMode import CompositeMode, StringMode, ArrayMode
from nodes.MonadicOperation import MonadicOperation
from nodes.Operand import Operand
from nodes.Operation import Operation
from nodes.Program import Program
from nodes.Identifier import Identifier
from nodes.Range import Range
from nodes.ReferenceMode import ReferenceMode
from nodes.SynonymDeclaration import SynonymDeclaration
from nodes.SynonymStatement import SynonymStatement
from nodes.Location import Location
from nodes.DereferencedLocation import DereferencedLocation
from nodes.StringElement import StringElement
from nodes.StringSlice import StringSlice
from nodes.ArrayElement import ArrayElement
from nodes.ArraySlice import ArraySlice

class Parser:

    tokens = Tokenizer.tokens
    reserved = Tokenizer.reserved

    # Program and Statement

    def p_program(self, p):
        'program : statement_list'
        p[0] = Program(p[1])

    def p_statement_list(self,p):
        'statement_list : statement statement_nullable'
        if len(p) == 3:
            if p[2] is not None:
                p[0] = p[2]
                p[0].append(p[1])
            else:
                p[0] = [p[1]]
        else:
            pass

    def p_statement_nullable(self, p):
        '''statement_nullable : statement statement_nullable
                              | empty'''
        if len(p) == 3:	
            if p[2] is not None:
                p[0] = p[2]
                p[0].append(p[1])
            else:
                p[0] = [p[1]]
        else:
            pass

	# TODO: procedure_statement, action_statement
    def p_statement(self, p):
        '''statement : declaration_statement
                     | synonym_statement
                     | newmode_statement'''
        p[0] = p[1]


    # '''
    # SYNONYM STATEMENT
    # '''

    def p_synonym_statement(self,p):
        '''synonym_statement : SYN synonym_list SEMI'''
        p[0] = SynomymStatement(p[2])

    def p_synonym_list(self,p):
        '''synonym_list : synonym_definition
                        | synonym_definition COMMA synonym_list'''
        p[0] = [p[1]]
        if(len(p) > 2):
            p[0].append(p[3])

    # Substituido constant_expression por expression, jah que eh igual
	# 'constante_expression : expression'

    def p_synonym_definition(self,p):
        '''synonym_definition : identifier_list mode ASSIGN expression
                              | identifier_list ASSIGN expression'''
        p[0] = SynonymDeclaration(p[1],
                                  p[2] if len(p) >= 5 else None,
                                  p[4] if len(p) >= 5 else p[3],)


    # '''
    # DECLARATION STATEMENT (aka dcl)
    # '''

    def p_declaration_statement(self, p):
        'declaration_statement : DCL declaration_list SEMI'
        p[0] = DeclarationStatement(p[2])

    def p_declaration_list(self, p):
        '''declaration_list : declaration
                            | declaration COMMA declaration_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = [p[1]]
            p[0].append(p[3])

    def p_declaration(self,p):
        '''declaration : identifier_list mode initialization
                       | identifier_list mode'''
        p[0] = Declaration(p[1],p[2], p[3] if len(p) > 3 else None)

    def p_initialization(self,p):
        '''initialization : ASSIGN expression'''
        p[0] = p[2]

    def p_identifier_list(self,p):
        '''identifier_list : ID
                           | ID COMMA identifier_list'''
        if len(p) == 2:
            p[0] = [Identifier(p[1])]
        elif len(p) > 3:
            p[0] = p[3]
            p[0].append(Identifier(p[1]))


    # '''
    # NEWMODE STATEMENT (aka type)
    # '''

    def p_newmode_statement(self,p):
        '''newmode_statement : TYPE newmode_list SEMI'''
        p[0] = NewModeStatement(p[2])

    def p_newmode_list(self,p):
        '''newmode_list : mode_definition
                        | mode_definition COMMA newmode_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = [p[1]]
            p[0].append(p[3])

    def p_mode_definition(self,p):
        '''mode_definition : identifier_list ASSIGN mode'''
        p[0] = ModeDefinition(p[1],p[3])

    def p_mode(self,p):
        '''mode : mode_name
                | discrete_mode
                | reference_mode
                | composite_mode'''
        p[0] = p[1]

    def p_mode_name(self,p):
        '''mode_name : ID'''
        p[0] = ModeName(p[1])

	# Discrete Mode

    def p_discrete_mode(self,p):
        '''discrete_mode : integer_mode
                         | boolean_mode
                         | character_mode
                         | discrete_range_mode'''
        p[0] = p[1]

    def p_discrete_mode_name(self,p):
        '''discrete_mode_name : ID'''
        p[0] = DiscreteModeName(p[1])

    def p_integer_mode(self,p):
        'integer_mode : INT'
        p[0] = IntegerMode()

    def p_boolean_mode(self,p):
        'boolean_mode : BOOL'
        p[0] = BooleanMode()

    def p_character_mode(self,p):
        'character_mode : CHAR'
        p[0] = CharMode()

    # Discrete Range Mode

    def p_discrete_range_mode(self,p):
        '''discrete_range_mode : discrete_mode_name LPAREN literal_range RPAREN
                               | discrete_mode LPAREN literal_range RPAREN'''
        p[0] = DiscreteRangeMode(p[1],p[3])

    def p_literal_range(self,p):
        '''literal_range : lower_bound COLON upper_bound'''
        p[0] = Range(p[1],p[3])

    def p_lower_bound(self,p):
        '''lower_bound : expression'''
        p[0] = p[1]
    def p_upper_bound(self, p):
        '''upper_bound : expression'''
        p[0] = p[1]

    # Reference Mode

    def p_reference_mode(self,p):
        '''reference_mode : REF mode'''
        p[0] = ReferenceMode(p[2])

    # Composite Mode

    def p_composite_mode(self,p):
        '''composite_mode : string_mode
                          | array_mode'''
        p[0] = CompositeMode(p[1])

    def p_string_mode(self,p):
        '''string_mode : CHARS LBRACKET string_length RBRACKET'''
        p[0] = StringMode(p[3])

    def p_string_length(self,p):
        '''string_length : integer_literal'''
        p[0] = p[1]

    def p_array_mode(self,p):
        '''array_mode : ARRAY LBRACKET index_mode_list RBRACKET element_mode'''
        p[0] = ArrayMode(p[3],p[5])

    def p_index_mode_list(self,p):
        '''index_mode_list : index_mode
                           | index_mode COMMA index_mode_list'''
        p[0] = [p[1]]
        if(len(p) > 2):
            p[0].append(p[3])

    def p_index_mode(self,p):
        '''index_mode : discrete_mode
                      | literal_range'''
        p[0] = p[1]

    def p_element_mode(self,p):
        '''element_mode : mode'''
        p[0] = p[1]

	# '''
	# LOCATION
	# '''
	
	def p_location(self, p):
		'''location : ID
				    | dereferenced_reference
				    | string_element
				    | string_slice
				    | array_element
				    | array_slice
				    | call_action'''
		p[0] = Location(p[1])
	
	def p_dereferenced_reference(self,p):
		'''dereferenced_reference : location ARROW'''
		p[0] = DereferencedLocation(p[1])
	
	def p_string_element(self,p):
		'''string_element : string_location LBRACKET start_element LBRACKET'''
		p[0] = StringElement(p[1],p[3])
		
	def p_start_element(self,p):
		'''start_element : integer_expression'''
		p[0] = p[1]
	
	def p_string_slice(self,p):
		'''string_slice : string_location LBRACKET left_element COLON right_element RBRACKET'''
		p[0] = StringSlice(p[1],p[3],p[5])
		
	def p_string_location(self,p):
		'''string_location : ID'''
		p[0] = p[1]
		
	def p_left_element(self,p):
		'''left_element : integer_expression'''
		p[0] = p[1]
		
	def p_right_element(self,p):
		'''right_element : integer_expression'''
		p[0] = p[1]

	def p_array_element(self,p):
		'''array_element : array_location LBRACKET expression_list RBRACKET'''
		p[0] = ArrayElement(p[1],p[3])
		
	def p_expression_list(self,p):
		'''expression_list : expression
						   | expression COMMA expression_list'''
		if len(p) == 2:
			p[0] = p[1]
		else:
			p[0] = p[1] + [p[3]]

	def p_array_slice(self,p):
		'''array_slice : array_location LBRACKET lower_bound COLON upper_bound RBRACKET'''
		p[0] = ArraySlice(p[1],p[3],p[5])	
	
	def p_array_location(self,p):
		'''array_location : location'''
		p[0] = p[1]

    # '''
    # EXPRESSION
    # '''

    # TODO: FALTA CONDITIONAL EXPRESSION
    def p_expression(self,p):
        '''expression : operand0'''
        p[0] = Expression(p[1])

    # OPERAND
    def p_operand0(self,p):
        '''operand0 : operand1
                    | operand0 operator1 operand1'''
        if len(p) > 2:
            p[0] = Operation(p[1], p[2], p[3])
        else:
            p[0] = p[1]
    def p_operand1(self,p):
        '''operand1 : operand2
                    | operand1 operator2 operand2'''
        if len(p) > 2:
            p[0] = Operation(p[1], p[2], p[3])
        else:
            p[0] = p[1]

    def p_operand2(self,p):
        '''operand2 : operand3
                    | operand2 arithmetic_multiplicative_operator operand3'''
        if len(p) > 2:
            p[0] = Operation(p[1], p[2], p[3])
        else:
            p[0] = p[1]


    # operand3 : integer_literal, regra desnecessaria e causa reduce/reduce conflict
    def p_operand3(self,p):
        '''operand3 : monadic_operator operand4
                    | operand4'''
        if len(p) > 2:
            p[0] = MonadicOperation(p[1], p[2])
        else:
            p[0] = p[1]


    def p_operand4(self, p):
        '''operand4 : primitive_value'''
        p[0] = Operand(p[1])

    def p_arithmetic_multiplicative_operator(self,p):
        '''arithmetic_multiplicative_operator : TIMES
                                              | DIVIDE
                                              | MODULO'''
        p[0] = p[1]

    def p_monadic_operator(self,p):
        '''monadic_operator : MINUS
                            | NOT'''
        p[0] = p[1]

    # OPERATOR
    def p_operator1(self,p):
        '''operator1 : relational_operator
                    | membership_operator'''
        p[0] = p[1]

    def p_operator2(self,p):
        '''operator2 : arithmetic_additive_operator
                     | string_concatenation_operator'''
        p[0] = p[1]

    def p_arithmetic_additive_operator(self,p):
        '''arithmetic_additive_operator : PLUS
                                        | MINUS'''
        p[0] = p[1]

    def p_string_concatenation_operator(self,p):
        '''string_concatenation_operator : CONCAT'''
        p[0] = p[1]

    def p_relational_operator(self,p):
        '''relational_operator : AND
                               | OR
                               | EQUAL
                               | NOTEQ
                               | GREATER
                               | GTEQUAL
                               | LESS
                               | LTEQUAL'''
        p[0] = p[1]

    def p_membership_operator(self,p):
        '''membership_operator : IN'''
        p[0] = p[1]



    # '''
    # PRIMITIVE VALUES
    # '''
    # TODO: SOH LITERAIS POR ENQUANTO

    def p_primitive_value(self,p):
        '''primitive_value : literal'''
        p[0] = p[1]

    def p_literal(self,p):
        '''literal : integer_literal
                   | boolean_literal
                   | character_literal
                   | empty_literal
                   | character_string_literal'''
        p[0] = p[1]
    def p_integer_literal(self,p):
        '''integer_literal : ICONST'''
        p[0] = IntegerLiteral(p[1])

    def p_boolean_literal(self, p):
        '''boolean_literal : TRUE
                           | FALSE'''
        p[0] = BoolLiteral(p[1])

    def p_character_literal(self, p):
        '''character_literal : CCONST'''
        p[0] = CharLiteral(p[1])


    def p_empty_literal(self,p):
        '''empty_literal : NULL'''
        p[0] = NullLiteral(p[1])

    def p_character_string_literal(self,p):
        '''character_string_literal : SCONST'''
        p[0] = StringLiteral(p[1])

    # empty
    def p_empty(self, p):
        'empty :'
        pass

    # Error rule for syntax errors
    def p_error(self, error):
        print("Syntax error in input!")

    def build(self):
        self.parser = yacc.yacc(module=self)
        
