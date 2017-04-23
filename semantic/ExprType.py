class ExprType(object):
    def __init__(self, type):
        self.type = type


int_type = ExprType("int")
bool_type = ExprType("bool")
char_type = ExprType("char")
string_type = ExprType("string")
