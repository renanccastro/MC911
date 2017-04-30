from .AST import AST

class BooleanExpression(AST):
    _fields = ['left', 'operator', 'right']
