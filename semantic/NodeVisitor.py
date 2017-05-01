from nodes.AST import AST
from nodes.DiscreteMode import *
from nodes.Literal import StringLiteral
from semantic.Environment import Environment
from semantic.ExprType import *
from semantic.SymbolTable import SymbolTable


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
                      "Unary operator '{}' not supported".format(op))
            return val.raw_type

    def raw_type_boolean(self, node, op, left, right):
        if hasattr(left, "raw_type") and hasattr(right, "raw_type"):
            if left.raw_type.type != right.raw_type.type:
                error(node.lineno,
                      "Binary operator '{}' does not have matching types".format(op))
            return left.raw_type

    def raw_type_binary(self, node, op, left, right):
        if hasattr(left, "raw_type") and hasattr(right, "raw_type"):
            left_type = left.raw_type
            right_type = right.raw_type
            if left_type.type == 'array':
                left_type = left.array_type
            if right_type.type == 'array':
                right_type = right.array_type
            if left_type.type != right_type.type:
                error(node.lineno,
                      "Binary operator '{}' does not have matching types".format(op))
            errside = None
            if op not in left_type.binary_ops:
                errside = "LHS"
            if op not in right_type.binary_ops:
                errside = "RHS"
            if errside is not None:
                error(node.lineno,
                      "Binary operator '{}' not supported on {} of expression".format(op, errside))
        return left_type

    def generic_visit(self,node):
        """
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)


    def visit_Program(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()
        for statement in node.statements: self.visit(statement)

    def visit_NewModeStatement(self, node):
        # TODO: AQUI DEVE PERCORRER E GUARDAR EM OUTRO MAPA OS NOVOS TIPOS DEFINIDOS
        mode_definition_list = node.mode_definition_list
        for mode_definition in mode_definition_list:
            self.visit(mode_definition)

    def visit_ModeDefinition(self, node):
        self.visit(node.mode)
        for obj in node.identifier_list:
            self.environment.add_local(obj.identifier, node.mode)

    def visit_SynonymStatement(self, node):
        for syn in node.synonym_list:
            self.visit(syn)

    def visit_SynonymDeclaration(self, node):
        self.visit(node.mode)
        self.visit(node.initialization)
        if 'const' not in repr(node.initialization.raw_type.true_type) :
            error(node.lineno, "Assignment value is not a constante expression")
        if node.mode is not None and (node.mode.raw_type.type != node.initialization.raw_type.type) :
            error(node.lineno, "Cannot assign '{}' expression to '{}' type"
                .format(node.initialization.raw_type.type, node.mode.raw_type.type))
        for obj in node.identifiers:
            if self.environment.find(obj.identifier):
                error(obj.lineno, "Duplicate definition of symbol '{}' on same scope".format(obj.identifier))
            self.environment.add_local(obj.identifier, node.initialization)

    def visit_DeclarationStatement(self, node):
        for declaration in node.declaration_list:
            self.visit(declaration)

    def visit_Declaration(self, node):
        self.visit(node.mode)
        self.visit(node.initialization)
        if node.initialization is not None and (node.mode.raw_type.type != node.initialization.raw_type.type) :
            error(node.lineno, "Cannot assign '{}' expression to '{}' type"
                .format(node.initialization.raw_type.type, node.mode.raw_type.type))
        for obj in node.identifier:
            if self.environment.find(obj.identifier):
                error(item.lineno, "Duplicate definition of symbol '{}' on same scope".format(obj.identifier))
            self.environment.add_local(obj.identifier,node.mode)
             
    def visit_IntegerMode(self, node):
        node.raw_type = self.environment.root['int']
    def visit_CharacterMode(self, node):
        node.raw_type = self.environment.root['char']
    def visit_BooleanMode(self, node):
        node.raw_type = self.environment.root['bool']
    def visit_NullMode(self, node):
        node.raw_type = self.environment.root['void']
        
    def visit_IntegerLiteral(self, node):
        node.raw_type = self.environment.root['const_int']
    def visit_CharacterLiteral(self, node):
        node.raw_type = self.environment.root['const_char']
    def visit_BooleanLiteral(self, node):
        node.raw_type = self.environment.root['const_bool']
    def visit_NullLiteral(self, node):
        node.raw_type = self.environment.root['const_void']
    def visit_StringLiteral(self, node):
        node.raw_type = self.environment.root['const_string']

    def visit_Location(self, node):
        self.visit(node.location)
        node.raw_type = node.location.raw_type

    def visit_StringElement(self, node):
        self.visit(node.location)
        node.raw_type = node.location._node.array_type

    def visit_Identifier(self, node):
        if self.environment.lookup(node.identifier) == None:
            error(node.lineno, "Identifier '{}' not defined".format(node.identifier))
        node._node = self.environment.lookup(node.identifier)
        node.raw_type = node._node.raw_type

    def visit_ProcedureStatement(self, node):

        # SETA AS COISAS AQUI POR CAUSA DAS CHAMADAS RECURSIVAS
        self.environment.add_local(node.name, node.definition)
        self.environment.functionsParameters.add(node.name, node.definition.parameters)
        if node.definition.returns is not None:
            self.visit(node.definition.returns)
            node.definition.raw_type = node.definition.returns.raw_type
        else:
            node.definition.raw_type = self.environment.root["void"]

        self.environment.push(node)
        self.visit(node.definition)
        self.environment.pop()


    def visit_ProcedureDefinition(self, node):
        for parameter in node.parameters:
            self.visit(parameter)

        if node.body is None or len(node.body) == 0:
            error(node.lineno, "No function body")
        for stmt in node.body:
            self.visit(stmt)


    def visit_ProcedureReturn(self, node):
        self.visit(node.mode)
        node.raw_type = node.mode.raw_type

    def visit_ProcedureParameter(self, node):
        self.visit(node.mode)
        for identifierObj in node.identifier_list:
            self.environment.add_local(identifierObj.identifier, node.mode)
        node.raw_type = node.mode.raw_type

    def visit_CompositeMode(self, node):
        self.visit(node.mode)
        node.raw_type = node.mode.raw_type
        if node.raw_type.type == 'array':
            node.array_type = node.mode.array_type

    def visit_StringMode(self, node):
        node.raw_type = self.environment.root["string"]

    def visit_ArrayMode(self, node):
        node.raw_type = self.environment.root["array"]
        self.visit(node.element_mode)
        node.array_type = node.element_mode.raw_type
        #   TODO: FALTA o index_mode_list

    # TODO: ArrayElement
    def visit_ArrayElement(self, node):
        self.visit(node.location)
        self.visit(node.expression)
        node.raw_type = node.location._node.array_type

    def visit_ModeName(self, node):
        self.visit(node.type)
        node.raw_type = node.type.raw_type
        if node.type.raw_type.type == 'array':
            node.array_type = node.type._node.array_type

    def visit_ActionStatement(self, node):
        self.visit(node.action)

    def visit_AssigmentAction(self, node):
        self.visit(node.location)
        self.visit(node.expression)
        loct_type = node.location.raw_type
        expr_type = node.expression.raw_type
        node.raw_type = node.expression.raw_type
        if 'const' in repr(loct_type.true_type) :
            error(node.lineno, "Cannot assign expression to constante type")
        if loct_type.type != expr_type.type :         
            error(node.lineno, "Cannot assign '{}' expression to '{}' type".format(expr_type.type,loct_type.type))        
        
    def visit_Expression(self, node):
        self.visit(node.value)
        node.raw_type = node.value.raw_type

    def visit_ConditionalExpression(self, node):
        self.visit(node.boolean_expression)
        self.visit(node.then_expression)
        self.visit(node.elsif_expression)
        self.visit(node.else_expression)

    def visit_BooleanExpression(self, node):
        self.visit(node.left)
        self.visit(node.right)
        node.raw_type = self.raw_type_boolean(node, node.operator, node.left, node.right)

    def visit_Operation(self, node):
        self.visit(node.operand0)
        self.visit(node.operand1)
        node.raw_type = self.raw_type_binary(node, node.operation, node.operand0, node.operand1)
        if (node.operand0.raw_type.true_type == node.operand1.raw_type.true_type):
            node.raw_type.true_type = node.operand0.raw_type.true_type
        else:
            node.raw_type.true_type = None 

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
        node._node = self.environment.lookup(node.name)
        node.raw_type = node._node.raw_type
        if node.raw_type is None:
            error(node.lineno, "Call to undefined function '{}'".format(node.name))
        funcParameters = self.environment.functionsParameters[node.name]
        # VERIFICA QUANTIDADE DE PARAMETROS
        if node.parameters is None:
            node.parameters = []
        if len(node.parameters) != len(funcParameters):
            error(node.lineno, "Wrong call to '{}'. Expected '{}' parameters, got '{}'".format(node.name, len(funcParameters), len(node.parameters)))
        # VERIFICA TIPOS DOS PARAMETROS
        for index, parameter in enumerate(node.parameters):
            self.visit(parameter)
            if parameter.raw_type.type != funcParameters[index].raw_type.type:
                error(node.lineno,
                      "Wrong call to '{}'. Expected '{}' parameter, got '{}' on parameter number {}"
                      .format(node.name, funcParameters[index].raw_type.type, parameter.raw_type.type, index))
    def visit_BuiltinCall(self, node):
        # TODO: PARA CADA FUNCAO TEM UM TIPO DE RETORNO
        node.raw_type = self.environment.root[node.name]

        # TODO: DEVE VERIFICAR TAMBÉM SE OS PARAMETROS SAO DOS TIPOS CERTOS COM A FUNCAO
        for parameter in node.parameters:
            self.visit(parameter)

    def visit_StepEnumeration(self, node):
        self.visit(node.loop_counter)
        self.visit(node.start_value)
        self.visit(node.step_value)
        self.visit(node.end_value)
        counter_type = node.loop_counter.raw_type.type
        if self.environment.lookup(node.loop_counter) == None :
            error(node.lineno, "Identifier '{}' not defined".format(node.loop_counter))
        if counter_type != node.start_value.raw_type.type :
            error(node.lineno, "Cannot assign '{}' expression to '{}' type".format(node.start_value.raw_type.type, counter_type))        
        if node.step_value is not None and (counter_type != node.step_value.raw_type.type) :
            error(node.lineno, "Cannot assign '{}' expression to '{}' type".format(node.step_value.raw_type.type, counter_type))        
        if node.end_value is not None and (counter_type != node.end_value.raw_type.type) :
            error(node.lineno, "Cannot compare '{}' expression with '{}' expression".format(node.end_value.raw_type.type, counter_type))     
            
    # TODO: VERIFICAR NOS FORS SE A INICIALIZACAO EH DO MESMO TIPO QUE A VARIAVEL DE CONTROLE
    # TODO : discrete mode
 
# on going ...            
#    def visit_RangeEnumeration(self, node):
#        self.visit(node.loop_counter)
#        self.visit(mode)
#        counter_type = node.loop_counter.raw_type.type
#        if counter_type != node.mode.raw_type.type :            
#            error(node.lineno, "Cannot compare '{}' expression with '{}' expression".format(node.end_value.raw_type.type, counter_type))     
                
    
# IF SEMPRE EH UMA EXPRESSAO BOOLEANA, PQ TEM QUE TER COMPARADOR RELACIONAL !OK!
# ARRAY CRIA UM NOVO TIPO ARRAY E COLOCA COMO OUTRO ATRIBUTO O INT, por ex !OK!
# NAO VERIFICA A CHAMADA DE FUNCAO, mas da pra salvar em um mapa seguindo o mesmo esquema de stack, so que guardando a lista dos parametros !OK!
# declaracao de funcao interna nao da erro !OK!

# TODO Ow verifica aí plz se eu faço na hora de setar uma declaração de strings se eu seto ela como um array de char
# dcl m,n,s int, x int = 3;
# dcl str chars[20];
# dcl a array[0:20] int;
# m = n + s;
# a[0] = 12;
# a[1] = 13;
# Vê se isso rola fazer
# str[2]='b'

