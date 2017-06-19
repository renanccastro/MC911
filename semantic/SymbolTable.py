class SymbolTable(dict):
    """
    Class representing a symbol table. It should
    provide functionality for adding and looking
    up nodes associated with identifiers.
    """

    def __init__(self, decl=None):
        super().__init__()
        self.decl = decl
        self.lastNumber = 0

    def add(self, name, value):
        self[name] = value

    def addWithSize(self, name, size):
        self[name] = self.lastNumber
        self.lastNumber = self.lastNumber + size

    def getLastNumber(self):
        return self.lastNumber


    def lookup(self, name):
        return self.get(name, None)

    def return_type(self):
        if self.decl:
            return self.decl.mode
        return None
        
