from .AST import AST

class StringSlice(AST):
    _fields = ['location','left','right']
