from .AST import AST


class ProcedureStatement(AST):
    _fields = ['name', 'definition']
