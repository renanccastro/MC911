from .AST import AST


class BuiltinCall(AST):
    _fields = ['name', 'parameters']
