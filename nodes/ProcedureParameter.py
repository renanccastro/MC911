from .AST import AST


class ProcedureParameter(AST):
    _fields = ['identifier_list','mode','loc']
