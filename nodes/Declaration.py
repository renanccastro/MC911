from AST import AST


class Declaration(AST):
    # TODO: falta 'initialization'
    _fields = ['identifier', 'mode', 'initialization']
