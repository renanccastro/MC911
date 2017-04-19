from .AST import AST

class ValueArraySlice(AST):
    _fields = ['array_primitive_value','lower','upper']
