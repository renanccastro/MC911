from nodes.AST import AST
import sys

k = 0

class NodeVisitor(object) :
    
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
            
    def generic_visit(self,node):
        """
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        global k
        for field in getattr(node,"_fields"):
            print(field)
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        k = k + 1
                        for n in range(k):
                            sys.stdout.write('-')
                        self.visit(item)
            elif isinstance(value, AST):
                k = k + 1
                for n in range(k):
                    sys.stdout.write('-')
                self.visit(value)
        k = k - 1
            
