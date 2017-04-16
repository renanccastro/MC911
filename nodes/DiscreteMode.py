from .AST import AST


class IntegerMode(AST):
    _fields = []
class CharMode(AST):
    _fields = []
class BooleanMode(AST):
    _fields = []

class DiscreteModeName(AST):
    _fields = ['name']

class DiscreteMode(AST):
    _fields = ['mode']
