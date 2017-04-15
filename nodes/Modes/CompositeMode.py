from nodes.AST import AST

class CompositeMode(AST):
    _fields = ['mode']
class StringMode(AST):
    _fields = ['length']
class ArrayMode(AST):
    _fields = ['index_mode_list','element_mode']
