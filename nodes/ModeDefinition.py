from .AST import AST


class ModeDefinition(AST):
    _fields = ['identifier_list', 'mode']
