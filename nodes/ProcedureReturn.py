from .AST import AST


class ProcedureReturn(AST):
    _fields = ['mode','loc']
