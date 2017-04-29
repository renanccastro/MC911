from .AST import AST


class IntegerMode(AST):
    _fields = ['type']
class CharacterMode(AST):
    _fields = ['type']
class BooleanMode(AST):
    _fields = ['type']

class DiscreteModeName(AST):
    _fields = ['name']

class DiscreteMode(AST):
    _fields = ['mode']
