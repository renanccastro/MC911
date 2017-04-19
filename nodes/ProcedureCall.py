from .AST import AST


class ProcedureCall(AST):
    _fields = ['name', 'parameters']
