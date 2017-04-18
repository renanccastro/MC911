from .AST import AST


class ElsifExpression(AST):
    _fields = ['boolean_expression','then_expression']
