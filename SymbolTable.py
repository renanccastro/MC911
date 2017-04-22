class SymbolTable(dict):
    """
    Class representing a symbol table. It should
    provide functionality for adding and looking
    up nodes associated with identifiers.
    """

    def __init__(self, decl=None):
        super().__init__()
        self.decl = decl

    def add(self, name, value):
        self[name] = value

    def lookup(self, name):
        return self.get(name, None)

    def return_type(self):
        if self.decl:
            return self.decl.mode
        return None
        
