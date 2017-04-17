from .AST import AST


class Declaration(AST):
    _fields = ['identifier', 'mode', 'initialization']
