from .AST import AST

class ArraySlice(AST):
    _fields = ['location','lower','upper']
