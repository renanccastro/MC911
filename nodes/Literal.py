from .AST import AST


class CharacterLiteral(AST):
    _fields = ['value','type']
class BooleanLiteral(AST):
    _fields = ['value','type']
class IntegerLiteral(AST):
    _fields = ['value','type']
class NullLiteral(AST):
    _fields = []
class StringLiteral(AST):
    _fields = ['value','type']
