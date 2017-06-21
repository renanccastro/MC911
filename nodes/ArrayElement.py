from .AST import AST

class ArrayElement(AST):
    _fields = ['location','expression_list']
