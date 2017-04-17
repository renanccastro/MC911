from .AST import AST


class SynonymDeclaration(AST):
    _fields = ['identifiers', 'mode', 'initialization']
