from nodes.AST import AST
from nodes.DiscreteMode import *
from nodes.Literal import StringLiteral
from semantic.Environment import Environment
from semantic.ExprType import *
from semantic.SymbolTable import SymbolTable

k = 1


def error(lineno, param):
    print("{}, on line {}.".format(param, lineno))
    exit()


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

    def raw_type_unary(self, node, op, val):
        if hasattr(val, "raw_type"):
            if op not in val.raw_type.unary_ops:
                error(node.lineno,
                      "Unary operator {} not supported".format(op))
            return val.raw_type

    def raw_type_binary(self, node, op, left, right):
        if hasattr(left, "raw_type") and hasattr(right, "raw_type"):
            if left.raw_type != right.raw_type:
                error(node.lineno,
                      "Binary operator {} does not have matching types".format(op))
                return left.raw_type
            errside = None
            if op not in left.raw_type.binary_ops:
                errside = "LHS"
            if op not in right.raw_type.binary_ops:
                errside = "RHS"
            if errside is not None:
                error(node.lineno,
                      "Binary operator {} not supported on {} of expression".format(op, errside))
        return left.raw_type

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
            self.visit(mode_definition)

    def visit_ModeDefinition(self, node):
        self.visit(node.mode)
        for obj in node.identifier_list:
            self.environment.add_local(obj.identifier, node.mode.raw_type)

    def visit_SynonymStatement(self, node):
        # Visit all of the synonyms
        for syn in node.synonym_list:
            self.visit(syn)

    def visit_SynonymDeclaration(self, node):
        self.visit(node.mode)
        for obj in node.identifiers:
            if self.environment.find(obj.identifier):
                error(obj.lineno, "Duplicate definition of symbol {} on same scope".format(obj.identifier))
            self.environment.add_local(obj.identifier, node.mode.raw_type)

    def visit_DeclarationStatement(self, node):
        for declaration in node.declaration_list:
            self.visit(declaration)

    def visit_Declaration(self, node):
        variable_list = node.identifier
        self.visit(node.mode)
        for item in variable_list:
            variable = item.identifier
            if self.environment.find(variable):
                error(item.lineno, "Duplicate definition of symbol {} on same scope".format(variable))
            self.environment.add_local(variable,node.mode.raw_type)
            print (variable)
        # TODO: VERIFICAR SE A INICIALIZACAO EH DO MESMO TIPO QUE A DECLARACAO
        self.visit(node.initialization)

    def visit_IntegerMode(self, node):
        node.raw_type = self.environment.lookup('int')
    def visit_CharLiteral(self, node):
        node.raw_type = self.environment.lookup('char')
    def visit_BoolLiteral(self, node):
        node.raw_type = self.environment.lookup('bool')
    def visit_IntegerLiteral(self, node):
        node.raw_type = self.environment.lookup('int')
    def visit_NullLiteral(self, node):
        node.raw_type = self.environment.lookup('null')
    def visit_StringLiteral(self, node):
        node.raw_type = self.environment.lookup('string')

    def visit_Location(self, node):
        self.visit(node.location)
        node.raw_type = node.location.raw_type

    def visit_StringElement(self, node):
        self.visit(node.location)
        node.raw_type = node.location.raw_type

    def visit_Identifier(self, node):
        if self.environment.lookup(node.identifier) == None:
            error(node.lineno, "Identifier '{}' not defined".format(node.identifier))
        node.raw_type = self.environment.lookup(node.identifier)

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
        self.visit(node.mode)
        for identifierObj in node.identifier_list:
            self.environment.add_local(identifierObj.identifier, node.mode.raw_type)

    def visit_CompositeMode(self, node):
        self.visit(node.mode)
        node.raw_type = node.mode.raw_type

    def visit_StringMode(self, node):
        node.raw_type = self.environment.root["string"]

    def visit_ArrayMode(self, node):
        node.raw_type = self.environment.root["array"]
        self.visit(node.element_mode)
        node.array_type = node.element_mode.raw_type
        #   TODO: FALTA o index_mode_list



    def visit_ModeName(self, node):
        self.visit(node.type)
        node.raw_type = node.type.raw_type

    def visit_ActionStatement(self, node):
        self.visit(node.action)

    def visit_AssigmentAction(self, node):
        self.visit(node.location)
        self.visit(node.expression)
        # TODO: VERIFICAR SE O LHS TEM O MESMO TIPO DO RHS
        node.raw_type = node.expression.raw_type

    def visit_Expression(self, node):
        self.visit(node.value)
        node.raw_type = node.value.raw_type

    def visit_ConditionalExpression(self, node):
        self.visit(node.boolean_expression)
        self.visit(node.then_expression)
        self.visit(node.elsif_expression)
        self.visit(node.else_expression)

    def visit_Operation(self, node):
        self.visit(node.operand0)
        self.visit(node.operand1)
        node.raw_type = self.raw_type_binary(node, node.operation, node.operand0, node.operand1)

    def visit_MonadicOperation(self, node):
        self.visit(node.operand)
        node.raw_type = self.raw_type_unary(node, node.operation, node.operand)

    def visit_Operand(self, node):
        self.visit(node.value)
        node.raw_type = node.value.raw_type

    def visit_CallAction(self, node):
        self.visit(node.call)
        node.raw_type = node.call.raw_type

    def visit_ProcedureCall(self, node):
        node.raw_type = self.environment.lookup(node.name)

        # TODO: DEVE VERIFICAR TAMBÉM SE OS PARAMETROS SAO DOS TIPOS CERTOS COM A FUNCAO
        for parameter in node.parameters:
            self.visit(parameter)

    def visit_BuiltinCall(self, node):
        node.raw_type = null_type

        # TODO: DEVE VERIFICAR TAMBÉM SE OS PARAMETROS SAO DOS TIPOS CERTOS COM A FUNCAO
        for parameter in node.parameters:
            self.visit(parameter)



# TODO: VERIFICAR AS OPERACOES DE ASSIGNMENT SE OS OPERADORES ESTAO CERTO

# IF SEMPRE EH UMA EXPRESSAO BOOLEANA, PQ TEM QUE TER COMPARADOR RELACIONAL
# ARRAY CRIA UM NOVO TIPO ARRAY E COLOCA COMO OUTRO ATRIBUTO O INT, por ex
# NAO VERIFICA A CHAMADA DE FUNCAO, mas da pra salvar em um mapa seguindo o mesmo esquema de stack, so que guardando a lista dos parametros
# declaracao de funcao interna nao da erro