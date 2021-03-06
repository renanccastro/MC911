import ply.yacc as yacc

from Tokenizer import Tokenizer
from nodes.Actions.CallAction import CallAction
from nodes.Actions.ExitAction import ExitAction
from nodes.Actions.ResultAction import ResultAction
from nodes.Actions.ReturnAction import ReturnAction
from nodes.BuiltinCall import BuiltinCall
from nodes.ConditionalExpression import ConditionalExpression
from nodes.Control.ForControl import ForControl
from nodes.Control.WhileControl import WhileControl
from nodes.ElsifExpression import ElsifExpression
from nodes.NewModeStatement import NewModeStatement
from nodes.AST import AST
from nodes.DeclarationStatement import DeclarationStatement
from nodes.Declaration import Declaration
from nodes.DiscreteMode import IntegerMode, BooleanMode, CharacterMode, DiscreteModeName
from nodes.DiscreteRangeMode import DiscreteRangeMode
from nodes.Expression import Expression
from nodes.Literal import IntegerLiteral, BooleanLiteral, CharacterLiteral, NullLiteral, StringLiteral
from nodes.ModeDefinition import ModeDefinition
from nodes.ModeName import ModeName
from nodes.Modes.CompositeMode import CompositeMode, StringMode, ArrayMode
from nodes.MonadicOperation import MonadicOperation
from nodes.Operand import Operand
from nodes.Operation import Operation
from nodes.ProcedureCall import ProcedureCall
from nodes.ProcedureDefinition import ProcedureDefinition
from nodes.ProcedureParameter import ProcedureParameter
from nodes.ProcedureReturn import ProcedureReturn
from nodes.ProcedureStatement import ProcedureStatement
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
from nodes.ReferencedLocation import ReferencedLocation
from nodes.ValueArrayElement import ValueArrayElement
from nodes.ValueArraySlice import ValueArraySlice
from nodes.ActionStatement import ActionStatement
from nodes.AssigmentAction import AssigmentAction
from nodes.AssigningOperator import AssigningOperator
from nodes.ConditionalClause import ConditionalClause
from nodes.DoAction import DoAction
from nodes.ControlPart import ControlPart
from nodes.BooleanExpression import BooleanExpression
from nodes.StepEnumeration import StepEnumeration
from nodes.RangeEnumeration import RangeEnumeration

class Parser:
    tokens = Tokenizer.tokens
    reserved = Tokenizer.reserved
    precedence = (
        ('left', 'AND', 'OR'),
        ('left', 'EQUAL', 'NOTEQ'),
        ('left', 'LTEQUAL', 'LESS', 'GREATER', 'GTEQUAL'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIMES', 'DIVIDE', 'MODULO'),
        ('right', 'UMINUS', 'UNOT'),            # Unary minus operator
    )

    # Program and Statement

    def p_program(self, p):
        'program : statement_list'
        p[0] = Program(p[1], lineno=p.lineno(1))

    def p_statement_list(self, p):
        'statement_list : statement statement_nullable'
        if len(p) == 3:
            if p[2] is not None:
                p[0] = [p[1]] + p[2]
#                p[0] = p[2]
#                p[0].append(p[1])
            else:
                p[0] = [p[1]]
        else:
            pass

    def p_statement_nullable(self, p):
        '''statement_nullable : statement statement_nullable
                              | empty'''
        if len(p) == 3:
            if p[2] is not None:
                p[0] = [p[1]] + p[2]
#                p[0] = p[2]
#                p[0].append(p[1])
            else:
                p[0] = [p[1]]
        else:
            pass

    def p_statement(self, p):
        '''statement : declaration_statement
                     | synonym_statement
                     | newmode_statement
                     | action_statement
                     | procedure_statement'''
        p[0] = p[1]

    # '''
    # SYNONYM STATEMENT
    # '''

    # <editor-fold desc="synonym_statement">
    def p_synonym_statement(self, p):
        '''synonym_statement : SYN synonym_list SEMI'''
        p[0] = SynonymStatement(p[2], lineno=p.lineno(1))

    def p_synonym_list(self, p):
        '''synonym_list : synonym_definition
                        | synonym_definition COMMA synonym_list'''
        p[0] = [p[1]]
        if (len(p) > 2):
            p[0].append(p[3])

        # Substituido constant_expression por expression, jah que eh igual
        # 'constante_expression : expression'

    def p_synonym_definition(self, p):
        '''synonym_definition : identifier_list mode ASSIGN expression
                              | identifier_list ASSIGN expression'''
        p[0] = SynonymDeclaration(p[1],
                                  p[2] if len(p) >= 5 else None,
                                  p[4] if len(p) >= 5 else p[3], lineno=p.lineno(1))

    # </editor-fold>


    # '''
    # DECLARATION STATEMENT (aka dcl)
    # '''

    # <editor-fold desc="declaration_statement">
    def p_declaration_statement(self, p):
        'declaration_statement : DCL declaration_list SEMI'
        p[0] = DeclarationStatement(p[2], lineno=p.lineno(1))

    def p_declaration_list(self, p):
        '''declaration_list : declaration
                            | declaration COMMA declaration_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) == 4:
            p[0] = [p[1]] + p[3]
#            p[0] = p[3]
#            p[0].append(p[1])

    def p_declaration(self, p):
        '''declaration : identifier_list mode initialization
                       | identifier_list mode'''
        p[0] = Declaration(p[1], p[2], p[3] if len(p) > 3 else None, lineno=p.lineno(1))

    def p_initialization(self, p):
        '''initialization : ASSIGN expression'''
        p[0] = p[2]

    def p_identifier_list(self, p):
        '''identifier_list : identifier
                           | identifier COMMA identifier_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) > 3:
            p[0] = [p[1]] + p[3]
#            p[0] = p[3]
#            p[0].append(Identifier(p[1]))

    def p_identifier(self, p):
        '''identifier : ID'''
        p[0] = Identifier(p[1], lineno=p.lineno(1))
    # </editor-fold>

    # '''
    # NEWMODE STATEMENT (aka type)
    # '''

    # <editor-fold desc="newmode_statement">
    def p_newmode_statement(self, p):
        '''newmode_statement : TYPE newmode_list SEMI'''
        p[0] = NewModeStatement(p[2], lineno=p.lineno(1))

    def p_newmode_list(self, p):
        '''newmode_list : mode_definition
                        | mode_definition COMMA newmode_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) > 3:
            p[0] = [p[1]] + p[3]
#            p[0] = p[3]
#            p[0].append(p[1])

    def p_mode_definition(self, p):
        '''mode_definition : identifier_list ASSIGN mode'''
        p[0] = ModeDefinition(p[1], p[3], lineno=p.lineno(1))

    # </editor-fold>

    # '''
    # PROCEDURE STATEMENT (aka proc)
    # '''
    
    # <editor-fold desc="procedure_statement">
    def p_procedure_statement(self, p):
        '''procedure_statement : ID COLON procedure_definition'''
        p[0] = ProcedureStatement(p[1], p[3], lineno=p.lineno(1))

    def p_procedure_definition(self, p):
        '''procedure_definition : PROC LPAREN formal_parameter_list RPAREN result_spec SEMI statement_nullable END SEMI
                                | PROC LPAREN formal_parameter_list RPAREN SEMI statement_nullable END SEMI
                                | PROC LPAREN  RPAREN result_spec SEMI statement_nullable END SEMI
                                | PROC LPAREN  RPAREN SEMI statement_nullable END SEMI'''
        if p[3] == ")":
            p[0] = ProcedureDefinition([],
                                       p[4] if len(p) == 9 else None,
                                       p[len(p)-3],
                                       lineno=p.lineno(1))
        else:
            p[0] = ProcedureDefinition(p[3],
                                       p[5] if len(p) == 10 else None,
                                       p[len(p)-3],
                                       lineno=p.lineno(1))

    def p_formal_parameter_list(self, p):
        '''formal_parameter_list : formal_parameter
                                 | formal_parameter COMMA formal_parameter_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) > 3:
            p[0] = [p[1]] + p[3]
#            p[0] = p[3]
#            p[0].append(p[1])

    def p_formal_parameter(self, p):
        '''formal_parameter : identifier_list mode LOC
                            | identifier_list mode'''
        p[0] = ProcedureParameter(p[1], p[2], True if len(p) == 4 else False, lineno=p.lineno(1))

    # Removi parameter_spec pq nao faz sentido

    def p_result_spec(self, p):
        '''result_spec : RETURNS LPAREN mode LOC RPAREN
                       | RETURNS LPAREN mode RPAREN'''
        p[0] = ProcedureReturn(p[3], True if len(p) == 6 else False, lineno=p.lineno(1))

    # MODE
    def p_mode(self, p):
        '''mode : mode_name
                | discrete_mode
                | reference_mode
                | composite_mode'''
        p[0] = p[1]

    def p_mode_name(self, p):
        '''mode_name : identifier'''
        p[0] = ModeName(p[1], lineno=p.lineno(1))
    # </editor-fold>

    # Discrete Mode

    # <editor-fold desc="discrete_mode">
    def p_discrete_mode(self, p):
        '''discrete_mode : integer_mode
                         | boolean_mode
                         | character_mode
                         | discrete_range_mode'''
        p[0] = p[1]

    def p_discrete_mode_name(self, p):
        '''discrete_mode_name : identifier'''
        p[0] = DiscreteModeName(p[1], lineno=p.lineno(1))

    def p_integer_mode(self, p):
        'integer_mode : INT'
        p[0] = IntegerMode('int',lineno=p.lineno(1))

    def p_boolean_mode(self, p):
        'boolean_mode : BOOL'
        p[0] = BooleanMode('bool', lineno=p.lineno(1))

    def p_character_mode(self, p):
        'character_mode : CHAR'
        p[0] = CharacterMode('char', lineno=p.lineno(1))

    # </editor-fold>

    # Discrete Range Mode

    # <editor-fold desc="discrete_range_mode">
    def p_discrete_range_mode(self, p):
        '''discrete_range_mode : discrete_mode_name LPAREN literal_range RPAREN
                               | discrete_mode LPAREN literal_range RPAREN'''
        p[0] = DiscreteRangeMode(p[1], p[3], lineno=p.lineno(1))

    def p_literal_range(self, p):
        '''literal_range : lower_bound COLON upper_bound'''
        p[0] = Range(p[1], p[3], lineno=p.lineno(1))

    def p_lower_bound(self, p):
        '''lower_bound : expression'''
        p[0] = p[1]

    def p_upper_bound(self, p):
        '''upper_bound : expression'''
        p[0] = p[1]
    # </editor-fold>

    # Reference Mode

    def p_reference_mode(self, p):
        '''reference_mode : REF mode'''
        p[0] = ReferenceMode(p[2], lineno=p.lineno(1))

    # Composite Mode

    # <editor-fold desc="composite_mode">
    def p_composite_mode(self, p):
        '''composite_mode : string_mode
                          | array_mode'''
        p[0] = CompositeMode(p[1], lineno=p.lineno(1))

    def p_string_mode(self, p):
        '''string_mode : CHARS LBRACKET string_length RBRACKET'''
        p[0] = StringMode(p[3], lineno=p.lineno(1))

    def p_string_length(self, p):
        '''string_length : integer_literal'''
        p[0] = p[1]

    def p_array_mode(self, p):
        '''array_mode : ARRAY LBRACKET index_mode_list RBRACKET element_mode'''
        p[0] = ArrayMode(p[3], p[5], lineno=p.lineno(1))

    def p_index_mode_list(self, p):
        '''index_mode_list : index_mode
                           | index_mode COMMA index_mode_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) > 3:
            p[0] = [p[1]] + p[3]
#            p[0] = p[3]
#            p[0].append(p[1])

    def p_index_mode(self, p):
        '''index_mode : discrete_mode
                      | literal_range'''
        p[0] = p[1]

    def p_element_mode(self, p):
        '''element_mode : mode'''
        p[0] = p[1]
    # </editor-fold>

    # '''
    # LOCATION
    # '''

    # <editor-fold desc="location">

    def p_location(self, p):
        '''location : identifier
				    | dereferenced_reference
                    | array_element
				    | array_slice
				    | call_action'''
        p[0] = Location(p[1], lineno=p.lineno(1))

    def p_dereferenced_reference(self, p):
        '''dereferenced_reference : array_location ARROW'''
        p[0] = DereferencedLocation(p[1], lineno=p.lineno(1))

    # def p_string_element(self, p):
    #     '''string_element : identifier LBRACKET start_element RBRACKET'''
    #     p[0] = StringElement(p[1], p[3], lineno=p.lineno(1))

    # def p_start_element(self, p):
    #     '''start_element : expression'''
    #     p[0] = p[1]

    # def p_string_slice(self, p):
    #     '''string_slice : identifier LBRACKET left_element COLON right_element RBRACKET'''
    #     p[0] = StringSlice(p[1], p[3], p[5], lineno=p.lineno(1))

    # def p_left_element(self, p):
    #     '''left_element : expression'''
    #     p[0] = p[1]
    #
    # def p_right_element(self, p):
    #     '''right_element : expression'''
    #     p[0] = p[1]

    def p_array_element(self, p):
        '''array_element : array_location LBRACKET expression_list RBRACKET'''
        p[0] = ArrayElement(p[1], p[3], lineno=p.lineno(1))

    def p_expression_list(self, p):
        '''expression_list : expression
    					   | expression COMMA expression_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = p[3]
            p[0].append(p[1])

    def p_array_slice(self, p):
        '''array_slice : array_location LBRACKET literal_range RBRACKET'''
        p[0] = ArraySlice(p[1], p[3], lineno=p.lineno(1))

    def p_array_location(self, p):
        '''array_location : location'''
        p[0] = p[1]
    
    # </editor-fold>

    # '''
    # EXPRESSION
    # '''

    def p_expression(self, p):
        '''expression : operand0
                      | conditional_expression'''
        p[0] = Expression(p[1], lineno=p.lineno(1))
        
    def p_parenthesized_expression(self,p):
        '''parenthesized_expression : LPAREN expression RPAREN'''
        p[0] = p[2]

    # '''
    # Conditional Expression
    # '''
    # <editor-fold desc="conditional_expression">
    def p_conditional_expression(self, p):
        '''conditional_expression : IF expression then_expression else_expression FI
                                  | IF expression then_expression elsif_expression else_expression FI'''
        p[0] = ConditionalExpression(p[2], p[3], p[4] if len(p) > 6 else None, p[4] if len(p) <= 6 else p[5], lineno=p.lineno(1))

    def p_then_expression(self, p):
        '''then_expression : THEN expression'''
        p[0] = p[2]

    def p_else_expression(self, p):
        '''else_expression : ELSE expression'''
        p[0] = p[2]

    def p_elsif_expression(self, p):
        '''elsif_expression : ELSIF expression then_expression
                            | elsif_expression ELSIF expression then_expression'''
        if len(p) <= 4:
            p[0] = [ElsifExpression(p[2], p[3], lineno=p.lineno(1))]
        else:
            p[0] = p[1]
            p[0].append(ElsifExpression(p[3], p[4], lineno=p.lineno(1)))

    # </editor-fold>

    # '''
    # OPERAND
    # '''

    # <editor-fold desc="operand">
    def p_operand0(self, p):
        '''operand0 : operand1
                    | operand0 operator1 operand1'''
        if len(p) > 2:
            p[0] = BooleanExpression(p[1], p[2], p[3], lineno=p.lineno(1))
        else:
            p[0] = p[1]

    def p_operand1(self, p):
        '''operand1 : operand2
                    | operand1 operator2 operand2'''
        if len(p) > 2:
            p[0] = Operation(p[1], p[2], p[3], lineno=p.lineno(1))
        else:
            p[0] = p[1]

    def p_operand2(self, p):
        '''operand2 : operand3
                    | operand2 arithmetic_multiplicative_operator operand3'''
        if len(p) > 2:
            p[0] = Operation(p[1], p[2], p[3], lineno=p.lineno(1))
        else:
            p[0] = p[1]

    # 'operand3 : integer_literal' - regra desnecessaria e causa reduce/reduce conflict
    def p_operand3(self, p):
        '''operand3 : monadic_operator operand4
                    | operand4'''
        if len(p) > 2:
            p[0] = MonadicOperation(p[1], p[2], lineno=p.lineno(1))
        else:
            p[0] = p[1]

    def p_operand4(self, p):
        '''operand4 : array_location
                    | referenced_location
                    | primitive_value'''
        p[0] = Operand(p[1], lineno=p.lineno(1))
    # </editor-fold>


    # '''
    # OPERATOR
    # '''

    # <editor-fold desc="operator">
    def p_arithmetic_multiplicative_operator(self, p):
        '''arithmetic_multiplicative_operator : TIMES
                                              | DIVIDE
                                              | MODULO'''
        p[0] = p[1]

    def p_monadic_operator(self, p):
        '''monadic_operator : MINUS %prec UMINUS
                            | NOT %prec UNOT'''
        p[0] = p[1]

    def p_referenced_location(self, p):
        '''referenced_location : ARROW array_location'''
        p[0] = ReferencedLocation(p[2], lineno=p.lineno(1))

    def p_operator1(self, p):
        '''operator1 : membership_operator
                     | relational_operator'''
        p[0] = p[1]
    def p_relational_operator(self, p):
        '''relational_operator : AND
                               | OR
                               | EQUAL
                               | NOTEQ
                               | GREATER
                               | GTEQUAL
                               | LESS
                               | LTEQUAL'''
        p[0] = p[1]

    def p_operator2(self, p):
        '''operator2 : arithmetic_additive_operator
                     | string_concatenation_operator'''
        p[0] = p[1]

    def p_arithmetic_additive_operator(self, p):
        '''arithmetic_additive_operator : PLUS
                                        | MINUS'''
        p[0] = p[1]

    def p_string_concatenation_operator(self, p):
        '''string_concatenation_operator : CONCAT'''
        p[0] = p[1]


    def p_membership_operator(self, p):
        '''membership_operator : IN'''
        p[0] = p[1]

    # </editor-fold>

    # '''
    # PRIMITIVE VALUES
    # '''

    # <editor-fold desc="primitive_values">

    def p_primitive_value(self,p):
        '''primitive_value : literal
                           | value_array_element
                           | value_array_slice
                           | parenthesized_expression'''
        p[0] = p[1]

    def p_literal(self, p):
        '''literal : integer_literal
                   | boolean_literal
                   | character_literal
                   | empty_literal
                   | character_string_literal'''
        p[0] = p[1]
        
    def p_value_array_element(self,p):
        '''value_array_element : primitive_value LBRACKET expression_list RBRACKET'''
        p[0] = ValueArrayElement(p[1],p[3], lineno=p.lineno(1))
        
    def p_value_array_slice(self,p):
        '''value_array_slice : primitive_value LBRACKET expression COLON expression RBRACKET'''
        p[0] = ValueArraySlice(p[1],p[3],p[5], lineno=p.lineno(1))
    
    #def p_array_primitive_value(self,p):
    #    '''array_primitive_value : primitive_value'''
    #    p[0] = p[1]
        
    def p_integer_literal(self,p):
        '''integer_literal : ICONST'''
        p[0] = IntegerLiteral(p[1], 'int', lineno=p.lineno(1))

    def p_boolean_literal(self, p):
        '''boolean_literal : TRUE
                           | FALSE'''
        p[0] = BooleanLiteral(p[1], 'bool' , lineno=p.lineno(1))

    def p_character_literal(self, p):
        '''character_literal : CCONST
                             | HAT LPAREN ICONST RPAREN'''
        if len(p) == 2 :
            p[0] = CharacterLiteral(p[1], 'char', lineno=p.lineno(1))
        elif len(p) == 5 :
            p[0] = CharacterLiteral(chr(p[3]), 'char', lineno=p.lineno(1))
        else :
            pass

    def p_empty_literal(self,p):
        '''empty_literal : NULL'''
        p[0] = NullLiteral('null', lineno=p.lineno(1))

    def p_character_string_literal(self, p):
        '''character_string_literal : SCONST'''
        p[0] = StringLiteral(p[1], 'string', lineno=p.lineno(1))
    # </editor-fold>



    # '''
    # ACTION STATEMENT
    # '''

    def p_action_statement(self,p):
        '''action_statement : identifier COLON action SEMI
                            | action SEMI'''
        p[0] = ActionStatement(p[1] if len(p) == 5 else None,
                               p[3] if len(p) == 5 else p[1], lineno=p.lineno(1))

    def p_action(self,p):
        '''action : bracketed_action
                  | assignment_action
                  | call_action
                  | exit_action
                  | result_action
                  | return_action'''
        p[0] = p[1]
          
    def p_bracketed_action(self,p):
        '''bracketed_action : if_action
                            | do_action'''
        p[0] = p[1]
    
    def p_assignment_action(self,p):
        '''assignment_action : array_location assigning_operator expression'''
        if p[2].operator is not None:
            p[3].value = Operation(Operand(p[1], lineno=p.lineno(1)), p[2].operator, p[3].value, lineno=p.lineno(1))
        p[0] = AssigmentAction(p[1],p[2],p[3], lineno=p.lineno(1))

    def p_assigning_operator(self,p):
        '''assigning_operator : closed_dyadic_operator ASSIGN
                              | ASSIGN'''
        p[0] = AssigningOperator(p[1] if len(p) == 3 else None, '=', lineno=p.lineno(1))
    
    def p_closed_dyadic_operator(self,p):
        '''closed_dyadic_operator : arithmetic_additive_operator
                                  | arithmetic_multiplicative_operator
                                  | string_concatenation_operator'''
        p[0] = p[1]
        
    def p_if_action(self,p):
        '''if_action : IF expression then_clause else_clause FI
                     | IF expression then_clause FI'''
        p[0] = ConditionalClause(p[2],p[3], p[4] if len(p) == 6 else None, lineno=p.lineno(1))
    
    def p_then_clause(self,p):
        '''then_clause : THEN action_statement_list'''
        p[0] = p[2]

    def p_else_clause(self,p):
        '''else_clause : ELSE action_statement_list
                       | ELSIF expression then_clause else_clause
                       | ELSIF expression then_clause'''
        if len(p) == 3:
            p[0] = p[2]
        elif len(p) == 4:
            p[0] = ConditionalClause(p[2],p[3],None, lineno=p.lineno(1))
        elif len(p) == 5:
            p[0] = ConditionalClause(p[2],p[3],p[4], lineno=p.lineno(1))
        else:
            pass

    def p_action_statement_list(self,p):
        '''action_statement_list : action_statement action_statement_nullable'''
        if len(p) == 3:
            if p[2] is not None:
                p[0] = [p[1]] + p[2]
#                p[0] = p[2]
#                p[0].append(p[1])
            else:
                p[0] = [p[1]]
        else:
            pass
    
    def p_action_statement_nullable(self,p):
        '''action_statement_nullable : action_statement action_statement_nullable
                                     | empty'''    
        if len(p) == 3:
            if p[2] is not None:
                p[0] = [p[1]] + p[2]
#                p[0] = p[2]
#                p[0].append(p[1])
            else:
                p[0] = [p[1]]
        else:
            pass


    # '''
    # CALL ACTION
    # '''

    def p_call_action(self, p):
        '''call_action : procedure_call
                       | builtin_call'''
        p[0] = CallAction(p[1], lineno=p.lineno(1))

    def p_builtin_call(self, p):
        '''builtin_call : builtin_name LPAREN parameter_list RPAREN
                        | builtin_name LPAREN RPAREN'''
        p[0] = BuiltinCall(p[1],p[3] if len(p) == 5 else None, lineno=p.lineno(1))


    def p_builtin_name(self, p):
        '''builtin_name : ABS
                        | ASC
                        | NUM
                        | UPPER
                        | LOWER
                        | LENGTH
                        | READ
                        | PRINT'''
        p[0] = p[1]

    def p_procedure_call(self, p):
        '''procedure_call : ID LPAREN parameter_list RPAREN
                          | ID LPAREN RPAREN'''
        p[0] = ProcedureCall(p[1],p[3] if len(p) == 5 else None, lineno=p.lineno(1))

    def p_parameter_list(self, p):
        '''parameter_list : expression
                          | expression COMMA parameter_list'''
        if len(p) == 2:
            p[0] = [p[1]]
        elif len(p) > 3:
            p[0] = [p[1]] + p[3]
#            p[0] = p[3]
#            p[0].append(p[1])

    def p_exit_action(self, p):
        '''exit_action : EXIT identifier'''
        p[0] = ExitAction(p[2], lineno=p.lineno(1))

#    def p_label_id(self, p):
#        '''label_id : ID'''
#        p[0] = p[1]

    def p_return_action(self, p):
        '''return_action : RETURN result'''
        p[0] = ReturnAction(p[2], lineno=p.lineno(1))

    def p_result(self, p):
        '''result : expression
                  | empty'''
        p[0] = p[1]
    def p_result_action(self, p):
        '''result_action : RESULT expression'''
        p[0] = ResultAction(p[2], lineno=p.lineno(1))

    # '''
    # DO ACTION
    # '''
    
    def p_do_action(self,p):
        '''do_action : DO control_part SEMI action_statement_nullable OD
                     | DO action_statement_nullable OD'''
        if len(p) == 6:
            p[0] = DoAction(p[2],p[4], lineno=p.lineno(1))
        elif len(p) == 4:
            p[0] = DoAction(None,p[2], lineno=p.lineno(1))

    def p_control_part(self,p):
        '''control_part : for_control while_control 
                        | for_control   
                        | while_control'''
        p[0] = ControlPart(p[1], p[2] if len(p) == 3 else None)

    def p_for_control(self,p):
        '''for_control : FOR iteration'''
        p[0] = ForControl(p[2], lineno=p.lineno(1))
        
    def p_iteration(self,p):
        '''iteration : step_enumeration
                     | range_enumeration'''
        p[0] = p[1]

    def p_step_enumeration(self,p):
        '''step_enumeration : identifier ASSIGN expression step_value DOWN end_value
                            | identifier ASSIGN expression step_value end_value
                            | identifier ASSIGN expression DOWN end_value
                            | identifier ASSIGN expression end_value'''
        if len(p) == 5:
            p[0] = StepEnumeration(p[1],p[3],None,None,p[4], lineno=p.lineno(1))
        elif len(p) == 6:
            if p[4] == 'DOWN':
                p[0] = StepEnumeration(p[1],p[3],None,'DOWN',p[5], lineno=p.lineno(1))
            else:
                p[0] = StepEnumeration(p[1],p[3],p[4],None,p[5], lineno=p.lineno(1))
        else:
            p[0] = StepEnumeration(p[1],p[3],p[4],'DOWN',p[6], lineno=p.lineno(1))
            
    def p_step_value(self,p):
        '''step_value : BY expression'''
        p[0] = p[2]
    
    def p_end_value(self,p):
        '''end_value : TO expression'''
        p[0] = p[2]

    def p_range_enumeration(self,p):
        '''range_enumeration : identifier DOWN IN discrete_mode
                             | identifier IN discrete_mode'''
        if len(p) == 5:
            p[0] = RangeEnumeration(p[1], 'DOWN', p[4], lineno=p.lineno(1))
        else:
            p[0] = RangeEnumeration(p[1], None, p[3], lineno=p.lineno(1))
    
    def p_while_control(self,p):
        '''while_control : WHILE expression'''    
        p[0] = WhileControl(p[2], lineno=p.lineno(1))


    # empty
    def p_empty(self, p):
        'empty :'
        pass

    # Error rule for syntax errors
    def p_error(self, p):
        print("Syntax error in input at line: {0}".format(p.lineno))

    def build(self):
        self.parser = yacc.yacc(module=self)
        
