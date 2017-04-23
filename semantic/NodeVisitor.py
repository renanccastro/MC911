from nodes.AST import AST
from nodes.DiscreteMode import *
from nodes.Literal import StringLiteral
from semantic.Environment import Environment
from semantic.SymbolTable import SymbolTable

k = 1

class NodeVisitor(object) :
    
    def __init__ (self):
        self.environment = Environment()
        self.typemap = {
            "int": IntegerMode,
            "char": CharMode,
            "string": StringLiteral,
            "bool": BooleanMode
        }
    
    def visit(self,node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """
        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None
            
    # comentei aqui pra n imprimir um monte de coisas...
    def generic_visit(self,node):
        """
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        global k
        for field in getattr(node,"_fields"):
#            sys.stdout.write('-- '*k)
            value = getattr(node,field,None)
#            if str(value)[0] != '<' and str(value)[-1] != '>' :
#                print(str(field) + ' : ' + str(value))
#            else :
#                print(field)
            if isinstance(value, list):
                for item in value:
#                    print(item,value)
                    if isinstance(item,AST):
                        k = k + 1
                        self.visit(item)
            elif isinstance(value, AST):
                k = k + 1
                self.visit(value)
        k = k - 1

    def visit_Program(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        # Visit all of the statements
        for statement in node.statements: self.visit(statement)

    def visit_Declaration(self,node):
        variable_list = node.identifier
        node.symtab = self.environment.peek()
        for item in variable_list:
            variable = item.identifier
            node.symtab.add(variable,node.mode)
            print (variable)    
        
