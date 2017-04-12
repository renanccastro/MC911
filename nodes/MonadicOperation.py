from AST import AST


class MonadicOperation(AST):
    _fields = ['operation', 'operand']
