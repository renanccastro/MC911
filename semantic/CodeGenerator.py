import sys

from nodes.AST import AST
from nodes.ArrayElement import ArrayElement
from nodes.DiscreteMode import *
from nodes.Literal import StringLiteral
from nodes.Operation import Operation
from semantic.Environment import Environment
from semantic.ExprType import *
from semantic.SymbolTable import SymbolTable

k = 1

def error(lineno, param):
    print("{}, on line {}.".format(param, lineno))


class GeneratorEnvironment(Environment):
    def __init__(self, variablesScope):
        super()
        self.stack = variablesScope
        self.H = []
        self.labels = []
        self.code = []

    def add_label(self, label):
        self.labels.append(label)

    def label_index(self, label):
        return self.labels.index(label)

class CodeGenerator(object) :

    def generate(self,node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None


    def generic_visit(self, node):
        # print("Node of class {} has no method visit", node.__class__.__name__)
        """
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        if type(node) is list:
            for obj in node:
                self.generate(obj)
            return

        for field in getattr(node, "_fields"):
            value = getattr(node, field, None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, AST):
                        self.generate(item)
            elif isinstance(value, AST):
                self.generate(value)



    def visit_Program(self, node):
        self.environment = GeneratorEnvironment(node.environment.variablesScope)
        print(self.environment.stack)
        self.environment.code.append(('stp',))
        self.environment.code.append(('alc', node.symboltable.lastNumber))
        for statement in node.statements: self.generate(statement)
        self.environment.code.append(('dlc', node.symboltable.lastNumber))
        self.environment.code.append(('end',))


    def visit_Declaration(self, node):
        for idObj in node.identifier:
            if node.initialization is not None:
                self.generate(node.initialization)
                (scope, offset) = self.environment.lookupWithScope(idObj.identifier)
                if node.initialization.raw_type.true_type == "const_string":
                    self.environment.code.append(('ldr', scope, offset))
                    self.environment.code.append(('sts', node.initialization.value.index))
                else:
                    self.environment.code.append(('stv', scope, offset))


    def visit_ProcedureStatement(self, node):
        self.environment.add_label(node.name)
        self.environment.add_label("jumpafter_" + node.name)

        self.environment.code.append(('jmp', self.environment.label_index("jumpafter_" + node.name)))
        self.environment.code.append(('lbl', self.environment.label_index(node.name)))
        self.environment.code.append(('enf', node.staticLevel))
        self.environment.code.append(('alc', node.symboltable.lastNumber))
        self.generate(node.definition)
        self.environment.code.append(('dlc', node.symboltable.lastNumber))
        self.environment.code.append(('ret', node.staticLevel, node.parametersNumber))
        self.environment.code.append(('lbl', self.environment.label_index("jumpafter_" + node.name)))

    def visit_Operation(self, node):
        self.generate(node.operand0)
        self.generate(node.operand1)
        if node.raw_type.type == "int":
            if node.operation == "*":
                self.environment.code.append(('mul',))
            elif node.operation == "+":
                self.environment.code.append(('add',))
            elif node.operation == "-":
                self.environment.code.append(('sub',))
            elif node.operation == "/":
                self.environment.code.append(('div',))
            elif node.operation == "%":
                self.environment.code.append(('mod',))
        #TODO concat operation   
          
        
    def visit_MonadicOperation(self, node):
        self.generate(node.operand)
        if node.operation == "-":
            self.environment.code.append(('neg',))
        elif node.operation == "!":
            self.environment.code.append(('not',))

    def visit_ArrayElement(self, node):
        self.generate(node.location)
        for i in reversed(range(len(node.expression_list))):
            self.generate(node.expression_list[i])
            self.generate(node._node.mode.index_mode_list[i].lower)
            self.environment.code.append(('sub',))
            self.environment.code.append(('idx', node._node.mode.sizeArray[i]))

    def visit_NewModeStatement(self, mode):
        pass
    def visit_Identifier(self, node):
        (scope, offset) = self.environment.lookupWithScope(node.identifier)
        if node.raw_type.type == "array":
            self.environment.code.append(('ldr', scope, offset))
        else:
            self.environment.code.append(('ldv', scope, offset))

    def visit_ProcedureParameter(self, node):
        pass

    def visit_IntegerLiteral(self, node):
        self.environment.code.append(('ldc', node.value))
        
    def visit_BooleanLiteral(self, node):
        if node.value == "TRUE" :
            self.environment.code.append(('ldc', True)) 
        elif node.value == "FALSE" :
            self.environment.code.append(('ldc', False)) 

    def visit_CharacterLiteral(self, node):
        self.environment.code.append(('ldc', node.value))

    def visit_StringLiteral(self, node):
        index = -1
        try:
            index = self.environment.H.index(node.value)
        except ValueError:
            self.environment.H.append(node.value)
            index = len(self.environment.H) - 1
        node.index = index

    def visit_Operand(self, node):
        self.generate(node.value)
        if node.raw_type.true_type == "array":
            self.environment.code.append(('grc',))
        elif node.raw_type.true_type == "const_string":
            node.index = node.value.index

    def read(self, node):
        for expression in node.parameters:
            if expression.raw_type.true_type == "array":
                self.generate(expression)
                # AQUI, EU TIRO O GRC que veio do load da expressao
                self.environment.code.pop()
                self.environment.code.append(('rdv',))
                self.environment.code.append(('smv', 1))
            elif expression.raw_type.true_type == "string":
                self.generate(expression)
                self.environment.code.append(('rds',))
            else:
                self.environment.code.append(('rdv',))
                operand = expression.value
                location = operand.value
                identifierObj = location.location
                identifier = identifierObj.identifier
                (scope, offset) = self.environment.lookupWithScope(identifier)
                self.environment.code.append(('stv', scope, offset))

    def print(self, node):
        for expression in node.parameters:
            if expression.raw_type.true_type == "const_string":
                self.generate(expression.value)
                self.environment.code.append(('prc', expression.value.index))
            elif expression.raw_type.true_type == "string":
                self.generate(expression.value)
                self.environment.code.append(('prs',))
            elif expression.raw_type.type == "char":
                self.generate(expression.value)
                self.environment.code.append(('prv', 1))
            else:
                self.generate(expression.value)
                self.environment.code.append(('prv', 0))


    def visit_ProcedureCall(self, node):
        for expression in reversed(node.parameters):
            self.generate(expression)
        self.environment.code.append(('cfu', self.environment.label_index(node.name)))


    def visit_BuiltinCall(self, node):
        result = {
            'read': self.read,
            'print': self.print,
        }[node.name](node)

    def visit_AssigmentAction(self, node):
        self.generate(node.assigning_operator)
       
        if node.raw_type.type == "array":
            # TODO: POR ENQUANTO SO FAZ ASSIGNMENT DE 1 VALOR NO ARRAY
            # VER SE HA POSSIBILIDADE DE FAZER COM MAIS
            self.generate(node.location)
            self.generate(node.expression)
            self.environment.code.append(('smv', 1))
        elif node.raw_type.type == "ref":
            # TODO: assignment de ref
            pass
        elif node.raw_type.true_type == "const_string":
            self.generate(node.expression)
            self.environment.code.append(('sts', node.expression.index))
        else:
            self.generate(node.expression)
            (scope, offset) = self.environment.lookupWithScope(node.location.location.identifier)
            self.environment.code.append(('stv', scope, offset))

    def visit_BooleanExpression(self, node):
        self.generate(node.left)
        self.generate(node.right)
        if node.operator == '&&':
            self.environment.code.append(('and',))
        elif node.operator == '||':
            self.environment.code.append(('lor',))
        elif node.operator == '==':
            self.environment.code.append(('equ',))
        elif node.operator == '!=':
            self.environment.code.append(('neq',))
        elif node.operator == '>':
            self.environment.code.append(('grt',))
        elif node.operator == '>=':
            self.environment.code.append(('gre',))
        elif node.operator == '<':
            self.environment.code.append(('les',))
        elif node.operator == '<=':
            self.environment.code.append(('leq',))
            
            
    def visit_ElsifExpression(self, node):
        else_label = "else_label_{}".format((self.environment.labels))

        self.environment.add_label(else_label)
        endif_label = "endif_label_{}".format((self.environment.labels))
        self.environment.add_label(endif_label)        

        self.generate(node.boolean_expression)
        self.environment.code.append(('jof', self.environment.label_index(else_label)))
        self.generate(node.then_expression)
        self.environment.code.append(('ldc', False))
        self.environment.code.append(('jmp', self.environment.label_index(endif_label)))
        self.environment.code.append(('lbl', self.environment.label_index(else_label)))
        self.environment.code.append(('ldc', True))
        self.environment.code.append(('lbl', self.environment.label_index(endif_label)))

    def visit_ConditionalClause(self, node):
        else_label = "else_label_{}".format(len(self.environment.labels))
        self.environment.add_label(else_label)        
        endif_label = "endif_label_{}".format(len(self.environment.labels))
        self.environment.add_label(endif_label)        

        self.generate(node.boolean_expression)
        self.environment.code.append(('jof', self.environment.label_index(else_label)))
        self.generate(node.then_clause)
        self.environment.code.append(('jmp', self.environment.label_index(endif_label)))
        self.environment.code.append(('lbl', self.environment.label_index(else_label)))
        self.generate(node.else_clause)
        self.environment.code.append(('lbl', self.environment.label_index(endif_label)))

    def visit_ConditionalExpression(self, node):
        elsif_label = "elsif_label_{}".format(len(self.environment.labels))
        self.environment.add_label(elsif_label)
        # else_label = "else_label_" + len(self.labels)
        # self.environment.add_label(else_label)
        endif_label = "endif_label_{}".format((self.environment.labels))
        self.environment.add_label(endif_label)
        
        self.generate(node.boolean_expression)
        self.environment.code.append(('jof', self.environment.label_index(elsif_label)))
        self.generate(node.then_expression)
        self.environment.code.append(('jmp', self.environment.label_index(endif_label)))

        self.environment.code.append(('lbl', self.environment.label_index(elsif_label)))
        self.generate(node.elsif_expression)
        if(node.elsif_expression is not None):
            self.environment.code.append(('jof', self.environment.label_index(endif_label)))
        # self.environment.code.append(('lbl', self.environment.label_index(else_label)))
        self.generate(node.else_expression)
        self.environment.code.append(('lbl', self.environment.label_index(endif_label)))
        
    def visit_ActionStatement(self, node): 
        if node.identifier is not None:
            self.generate(node.identifier)
            action_label = "action_label_{}".format(len(self.environment.labels))
            self.environment.add_label(action_label)
            self.environment.code.append(('lbl', self.environment.label_index(action_label)))
        self.generate(node.action)            


