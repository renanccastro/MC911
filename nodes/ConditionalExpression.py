from .AST import AST


class ConditionalExpression(AST):
    _fields = ['boolean_expression','then_expression','elsif_expression','else_expression']
