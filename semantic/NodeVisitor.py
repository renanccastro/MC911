from nodes.AST import AST
from nodes.DiscreteMode import *
from nodes.Literal import StringLiteral
from semantic.Environment import Environment
from semantic.ExprType import *
from semantic.SymbolTable import SymbolTable

k = 1

class NodeVisitor(object) :

    def __init__ (self):
        self.environment = Environment()

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
        # Visit all statements
        for statement in node.statements: self.visit(statement)


    def visit_NewModeStatement(self, node):
        # TODO: AQUI DEVE PERCORRER E GUARDAR EM OUTRO MAPA OS NOVOS TIPOS DEFINIDOS
        mode_definition_list = node.mode_definition_list
        for mode_definition in mode_definition_list:
            for obj in mode_definition.identifier_list:
                self.environment.add_local(obj.identifier,ExprType(obj.identifier))

    def visit_SynonymStatement(self, node):
        # Visit all of the synonyms
        for syn in node.synonym_list:
            self.visit(syn)

    def visit_SynonymDeclaration(self, node):
        for obj in node.identifiers:
            self.environment.add_local(obj.identifier, ExprType(node.mode.type))

    def visit_DeclarationStatement(self, node):
        for declaration in node.declaration_list:
            self.visit(declaration)


    def visit_Declaration(self, node):
        variable_list = node.identifier
        for item in variable_list:
            variable = item.identifier
            self.environment.add_local(variable,self.environment.lookup(self.visit(node.mode)))
            print (variable)

    def visit_IntegerMode(self, node):
        return 'int'

    def visit_Location(self, node):
        self.visit(node.location)

    def visit_Identifier(self, node):
        if self.environment.lookup(node.identifier) == None:
            print("Erro! Identificador '{}' não definido na linha {}".format(node.identifier, node.lineno))
            exit()
        return node.identifier

    def visit_ProcedureStatement(self, node):
        self.environment.push(node)
        func_type = self.visit(node.definition)
        self.environment.pop()
        self.environment.add_local(node.name, func_type)

    def visit_ProcedureDefinition(self, node):
        for parameter in node.parameters:
            self.visit(parameter)
        for stmt in node.body:
            self.visit(stmt)
        return self.environment.lookup(self.visit(node.returns))

    def visit_ProcedureReturn(self, node):
        return self.visit(node.mode)

    def visit_ProcedureParameter(self, node):
        for identifierObj in node.identifier_list:
            self.environment.add_local(identifierObj.identifier,self.environment.lookup(self.visit(node.mode)))

    def visit_ModeName(self, node):
        return self.visit(node.type)

    def visit_ActionStatement(self, node):
        self.visit(node.action)

    def visit_AssigmentAction(self, node):
        self.visit(node.location)