from semantic.ExprType import *
from semantic.SymbolTable import SymbolTable


class Environment(object):
    def __init__(self):
        self.stack = []
        self.functionsParameters = SymbolTable()
        self.root = SymbolTable()
        self.stack.append(self.root)
        self.root.update({
            "int": int_type,
            "char": char_type,
            "string": string_type,
            "bool": bool_type,
            "array": array_type,
            "void": null_type,
            # const
            "const_int": const_int_type,
            "const_char": const_char_type,
            "const_string": const_string_type,
            "const_bool": const_bool_type,
            "const_array": const_array_type,
            "const_void": const_null_type,
            # bultin_functions
            "abs" : int_type,
            "asc" : int_type,
            "num" : int_type,
            "upper" : int_type,
            "lower" : int_type,
            "length" : int_type,
            "read" : null_type,
            "print" : null_type
        })
        
    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))
    def pop(self):
        self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def scope_level(self):
        return len(self.stack)
    def add_local(self, name, value):
        self.peek().add(name, value)
    def add_root(self, name, value):
        self.root.add(name, value)
    def lookup(self, name):
        for scope in reversed(self.stack):
            hit = scope.lookup(name)
            if hit is not None:
                return hit
        return None
    def find(self, name):
        if name in self.stack[-1]:
            return True
        else:
            return False
