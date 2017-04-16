from .AST import AST


class Operation(AST):
    _fields = ['operand0', 'operation', 'operand1']
