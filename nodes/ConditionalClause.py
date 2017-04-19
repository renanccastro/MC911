from .AST import AST

class ConditionalClause(AST):
    _fields = ['boolean_expression','then_clause','else_clause']
