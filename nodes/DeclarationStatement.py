from .AST import AST


class DeclarationStatement(AST):
    _fields = ['declaration_list']
