import sys

from nodes.AST import AST
from nodes.DiscreteMode import *
from nodes.Literal import StringLiteral
from semantic.Environment import Environment
from semantic.ExprType import *
from semantic.SymbolTable import SymbolTable

k = 1

def error(lineno, param):
    print("{}, on line {}.".format(param, lineno))


class GeneratorEnvironment(Environment):
    def __init__(self):
        super()
        self.stack = []
        self.root = SymbolTable()
        self.stack.append(self.root)
        self.H = []
        self.code = []

class CodeGenerator(object) :

    def __init__ (self):
        self.environment = GeneratorEnvironment()

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
        self.environment.code.append(('stp',))
        for statement in node.statements: self.generate(statement)
        self.environment.code.append(('end',))


    def visit_Declaration(self, node):
        for idObj in node.identifier:
            # tratar inicializacao de array alocando o tamanho dele
            size = 1
            if node.mode.size:
                size = node.mode.size

            self.environment.peek().addWithSize(idObj.identifier, size)
            self.environment.code.append(('alc', size))
            if node.initialization is not None:
                self.generate(node.initialization)
                hit, scope = self.environment.lookupWithScope(idObj.identifier)
                self.environment.code.append(('stv', scope, hit))


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

    def visit_Identifier(self, node):
        hit, scope = self.environment.lookupWithScope(node.identifier)
        self.environment.code.append(('ldv', scope, hit))

    def visit_IntegerLiteral(self, node):
        self.environment.code.append(('ldc', node.value))



    def read(self, node):
        self.environment.code.append(('rdv',))
        for expression in node.parameters:
            operand = expression.value
            location = operand.value
            identifierObj = location.location
            identifier = identifierObj.identifier
            self.environment.code.append(('stv', len(self.environment.stack) - 1, self.environment.lookup(identifier)))

    def print(self, node):
        for expression in node.parameters:
            if expression.raw_type.true_type == "const_string":
                operand = expression.value
                literal = operand.value
                string = literal.value
                index = -1
                try:
                    index = self.environment.H.index(string)
                except ValueError:
                    self.environment.H.append(string)
                    index = len(self.environment.H) - 1
                self.environment.code.append(('prc', index))
            elif expression.raw_type.type == "int":
                self.generate(expression.value)
                self.environment.code.append(('prv', 0))

    def visit_BuiltinCall(self, node):
        result = {
            'read': self.read,
            'print': self.print,
        }[node.name](node)




