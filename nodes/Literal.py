from .AST import AST


class CharLiteral(AST):
    _fields = ['value','type']
class BoolLiteral(AST):
    _fields = ['value','type']
class IntegerLiteral(AST):
    _fields = ['value','type']
class NullLiteral(AST):
    _fields = []
class StringLiteral(AST):
    _fields = ['value','type']
