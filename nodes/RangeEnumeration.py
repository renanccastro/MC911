from .AST import AST

class RangeEnumeration(AST):
    _fields = ['loop_counter','down','discrete_mode']
