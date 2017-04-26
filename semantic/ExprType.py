class ExprType(object):
    def __init__(self, type, binary_ops, unary_ops):
        self.binary_ops = binary_ops
        self.unary_ops = unary_ops
        self.type = type


int_type = ExprType("int", ['+', '-' , '*', '/', '%', '==', '!=', '>', '>=', '<', '>=', '<', '<='], ['-'])
bool_type = ExprType("bool", ['==', '!='], ['!'])
char_type = ExprType("char", ['==', '!='], [])
string_type = ExprType("string", ['+', '==', '!=', '&'], [])
null_type = ExprType("null", [], [])
array_type = ExprType("array", [], [])
