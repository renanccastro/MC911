class ExprType(object):

    def __init__(self, true_type, binary_ops, unary_ops, type):
        self.binary_ops = binary_ops
        self.unary_ops = unary_ops
        self.type = type
        self.true_type = true_type

int_type = ExprType("int", ['+', '-' , '*', '/', '%', '==', '!=', '>', '>=', '<', '>=', '<', '<='], ['-'], "int")
bool_type = ExprType("bool", ['==', '!='], ['!'], "bool")
pointer_type = ExprType("ref", ['==', '!='], [], "ref")
char_type = ExprType("char", ['==', '!='], [], "char")
string_type = ExprType("string", ['+', '==', '!=', '&'], [], "string")
null_type = ExprType("null", [], [], "null")
array_type = ExprType("array", [], [], "array")

const_int_type = ExprType("const_int", ['+', '-' , '*', '/', '%', '==', '!=', '>', '>=', '<', '>=', '<', '<='], ['-'], "int")
const_bool_type = ExprType("const_bool", ['==', '!='], ['!'], "bool")
const_char_type = ExprType("const_char", ['==', '!='], [], "char")
const_string_type = ExprType("const_string", ['+', '==', '!=', '&'], [], "string")
const_null_type = ExprType("const_null", [], [], "null")
const_array_type = ExprType("const_array", [], [], "array")

