from .AST import AST

class AssigmentAction(AST):
    _fields = ['location','assigning_operator','expression']
