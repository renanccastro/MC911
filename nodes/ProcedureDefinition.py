from .AST import AST


class ProcedureDefinition(AST):
    _fields = ['parameters', 'returns', 'body']
