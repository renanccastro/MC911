import sys

from nodes.AST import AST
from nodes.DiscreteMode import *
from nodes.Literal import StringLiteral
from semantic.Environment import Environment
from semantic.ExprType import *
from semantic.SymbolTable import SymbolTable

k = 1

def error(lineno, param):
    print("{}, on line {}.".format(param, lineno))

class NodeVisitor(object) :

    def __init__ (self):
        self.environment = Environment()

    def visit_print(self, node):
        global k
        sys.stdout.write('-- '*k)
        print(str(node.__class__.__name__) + ' : ')
        k = k + 1
        for field in dir(node):
            if field[0] == "_":
                continue
            sys.stdout.write('-- '*k)
            value = getattr(node, field, None)

            if type(value) in (int, float, bool, str):
                print(str(field) + ' : ' + str(value))
            else:
                print(field)
            if isinstance(value, list):
                sys.stdout.write('-- ' * k)
                print('[')
                for item in value:
                    if isinstance(item, AST):
                        k = k + 1
                        self.visit_print(item)
                    sys.stdout.write('-- ' * k)
                    print(',')
                sys.stdout.write('-- ' * k)
                print(']')
            elif isinstance(value, AST):
                k = k + 1
                self.visit_print(value)
            elif isinstance(value, ExprType):
                sys.stdout.write('-- ' * (k+1))
                print("type = {}".format(value.type))
        k = k - 2

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
            left_type = left.raw_type
            right_type = right.raw_type
            if hasattr(left,"array_type"):
                left_type = left.array_type
            if hasattr(right, "array_type"):
                right_type = right.array_type

            if left_type.type != right_type.type:
                error(node.lineno,
                      "Binary operator '{}' does not have matching types".format(op))
            return self.environment.root["bool"]

    def raw_type_binary(self, node, op, left, right):
        if hasattr(left, "raw_type") and hasattr(right, "raw_type"):
            left_type = left.raw_type
            right_type = right.raw_type
            if hasattr(left,"array_type"):
                left_type = left.array_type
            if hasattr(right, "array_type"):
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
        if type(node) is list:
            for obj in node:
                self.visit(obj)
            return

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
        node.symboltable = self.environment.peek()
        for statement in node.statements: self.visit(statement)

    def visit_NewModeStatement(self, node):
        mode_definition_list = node.mode_definition_list
        for mode_definition in mode_definition_list:
            self.visit(mode_definition)

    def visit_ModeDefinition(self, node):
        self.visit(node.mode)
        for obj in node.identifier_list:
            if self.environment.find(obj.identifier):
                error(obj.lineno, "Duplicate definition of type '{}' on same scope".format(obj.identifier))
            else:
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
        for obj in node.identifier:
            if self.environment.find(obj.identifier):
                error(node.lineno, "Duplicate definition of symbol '{}' on same scope".format(obj.identifier))
            node.scope  = len(self.environment.stack) - 2
            node.offset = self.environment.peek().lastNumber
            self.environment.add_local(obj.identifier,node.mode,
                                       size=node.mode.size,
                                       offset=node.offset,
                                       scope=node.scope)
            if node.initialization is not None and (node.mode.raw_type.type == 'ref') :
                if not hasattr(node.mode, "array_type") or not hasattr(node.initialization, "array_type") :
                    error(node.lineno, "Cannot assign '{}' type to '{}'"
                          .format(node.initialization.raw_type.type, node.mode.raw_type.type))
                    return
                if node.mode.array_type.type != node.initialization.array_type.type :
                    error(node.lineno, "Cannot assign '{}' ref type to '{}' ref type"
                        .format(node.initialization.array_type.type, node.mode.array_type.type))                        
        if node.initialization is not None and (node.mode.raw_type.type != node.initialization.raw_type.type) :
            if node.mode.raw_type.true_type == node.initialization.raw_type.type or\
                            node.initialization.raw_type.true_type == node.mode.raw_type.type:
                return
            else:
                error(node.lineno, "Cannot assign '{}' expression to '{}' type"
                    .format(node.initialization.raw_type.type, node.mode.raw_type.type))

    def visit_IntegerMode(self, node):
        node.size = 1
        node.raw_type = self.environment.root['int']
    def visit_CharacterMode(self, node):
        node.size = 1
        node.raw_type = self.environment.root['char']
    def visit_BooleanMode(self, node):
        node.size = 1
        node.raw_type = self.environment.root['bool']
    def visit_NullMode(self, node):
        node.size = 1
        node.raw_type = self.environment.root['void']

    def visit_IntegerLiteral(self, node):
        node.size = 1
        node.calculatedValue = node.value
        node.raw_type = self.environment.root['const_int']
    def visit_CharacterLiteral(self, node):
        node.size = 1
        node.raw_type = self.environment.root['const_char']
    def visit_BooleanLiteral(self, node):
        node.size = 1
        node.raw_type = self.environment.root['const_bool']
    def visit_NullLiteral(self, node):
        node.size = 1
        node.raw_type = self.environment.root['const_void']

    def visit_StringLiteral(self, node):
        node.raw_type = self.environment.root['const_string']

    def visit_Location(self, node):
        self.visit(node.location)
        node.raw_type = node.location.raw_type
        if hasattr(node.location, "_node"):
            node._node = node.location._node
        if hasattr(node.location, "array_type"):
            node.array_type = node.location.array_type
        if hasattr(node.location, "loc"):
            node.loc = node.location.loc

        if node.raw_type.type == 'ref' :
            if hasattr(node.location, "_node"):
                node.array_type = node.location._node.array_type
            elif hasattr(node.location, "array_type"):
                node.array_type = node.location.array_type
        if node.raw_type.true_type == 'const_int':
            node.calculatedValue = node.location.calculatedValue


    def visit_DereferencedLocation(self, node):
        self.visit(node.location)
        if hasattr(node.location, "_node"):
            node._node = node.location._node
        node.raw_type = node._node.raw_type
        if node.raw_type.type != "ref":
            error(node.lineno, "Cannot dereference variable of type {}".format(node._node.raw_type.type))
            sys.exit(1)

        node.array_type = node._node.array_type

    def visit_ReferencedLocation(self, node):
        self.visit(node.location)
        node.raw_type = self.environment.root["ref"]
        node.array_type = node.location.raw_type
        if hasattr(node.location, "_node"):
            node._node = node.location._node


    def visit_Identifier(self, node):
        if self.environment.lookup(node.identifier) == None:
            error(node.lineno, "Identifier '{}' not defined".format(node.identifier))
            node.raw_type = self.environment.root["void"]
        else:
            node._node = self.environment.lookup(node.identifier)
            node.raw_type = node._node.raw_type
            if hasattr(node._node, "array_type"):
                node.array_type = node._node.array_type
            if hasattr(node._node, "loc"):
                node.loc= node._node.loc
            if node.raw_type.true_type == "const_int":
                node.calculatedValue = node._node.calculatedValue

    def visit_ProcedureStatement(self, node):
        # SETA AS COISAS AQUI POR CAUSA DAS CHAMADAS RECURSIVAS
        if self.environment.find(node.name):
            error(node.lineno, "Duplicate definition of function '{}'".format(node.name))

        self.environment.add_local(node.name, node.definition)

        self.environment.functionsParameters.add(node.name, [])
        size = 0
        for parameter in node.definition.parameters:
            for identifierObj in parameter.identifier_list:
                self.visit(parameter.mode)
                self.environment.functionsParameters.get(node.name).append(identifierObj)
                if parameter.loc == True:
                    size = size + 1
                else:
                    size = size + parameter.mode.size
        node.parametersSize = size
        node.parametersNumber = len(self.environment.functionsParameters.get(node.name))
        if node.definition.returns is not None:
            self.visit(node.definition.returns)
            node.definition.raw_type = node.definition.returns.raw_type
            if hasattr(node.definition.returns, "array_type"):
                node.definition.array_type = node.definition.returns.array_type
        else:
            node.definition.raw_type = self.environment.root["void"]
        self.environment.push(node)
        node.staticLevel = len(self.environment.stack) - 2
        node.definition.staticLevel = node.staticLevel
        node.definition.functionName = node.name
        self.visit(node.definition)
        node.symboltable = self.environment.peek()
        self.environment.pop()

    def visit_ProcedureDefinition(self, node):
        for parameter in node.parameters:
            self.visit(parameter)

        while len(self.environment.variablesScope) < (node.staticLevel + 1):
                self.environment.variablesScope.append({})
        i = -2
        for parameter in node.parameters:
            for identifierObj in parameter.identifier_list:
                    if parameter.loc == True:
                        i= i - 1
                    else:
                        i = i - parameter.mode.size
                    self.environment.variablesScope[node.staticLevel][identifierObj.identifier] = (node.staticLevel, i)
        node.returnLocation = (node.staticLevel , (i-1))

        if node.body is None or len(node.body) == 0:
            error(node.lineno, "No function body")

        if node.returns is not None:
            node.returns.functionName = node.functionName
        if node.body is not None:
            for stmt in node.body:
                stmt.functionName = node.functionName
                stmt.returnLocation = node.returnLocation
                stmt.returnNode = node.returns
                self.visit(stmt)

    def visit_ProcedureReturn(self, node):
        self.visit(node.mode)
        if node.loc == True:
            node.mode.loc = True
        if hasattr(node.mode, "array_type"):
            node.array_type = node.mode.array_type
        node.raw_type = node.mode.raw_type

    def visit_ReturnAction(self, node):
        if not hasattr(node, "returnNode"):
            error(node.lineno, "Calling return outside function")
            sys.exit(1)
        functionReturnNode = node.returnNode
        if node.return_expression is not None:
            self.visit(node.return_expression)
            if functionReturnNode.raw_type.type != node.return_expression.raw_type.type:
                error(node.lineno, "Returning different types")
            elif functionReturnNode.raw_type.type == node.return_expression.raw_type.type and \
                 functionReturnNode.raw_type.type == 'ref' and \
                 functionReturnNode.array_type.type != node.return_expression.array_type.type:
                error(node.lineno, "Returning different ref types")

    def visit_ResultAction(self, node):
        if not hasattr(node, "returnNode"):
            error(node.lineno, "Calling result outside function")
            sys.exit(1)
        functionReturnNode = node.returnNode
        self.visit(node.result_expression)
        if functionReturnNode.raw_type.type != node.result_expression.raw_type.type:
            error(node.lineno, "Resulting different types")
        elif functionReturnNode.raw_type.type == node.result_expression.raw_type.type and \
             functionReturnNode.raw_type.type == 'ref' and \
             functionReturnNode.array_type.type != node.result_expression.array_type.type:
            error(node.lineno, "Resulting different ref types")
        pass

    def visit_ProcedureParameter(self, node):
        self.visit(node.mode)
        for identifierObj in node.identifier_list:
            if node.loc:
                node.mode.loc = node.loc
                identifierObj.loc = node.loc
            #     node.mode.array_type = node.mode.raw_type
            #     node.mode.raw_type = self.environment.root["ref"]

            identifierObj.raw_type = node.mode.raw_type
            identifierObj.mode = node.mode
            if hasattr(node.mode, "array_type"):
                identifierObj.array_type = node.mode.array_type

            self.environment.add_local(identifierObj.identifier,node.mode)
        node.raw_type = node.mode.raw_type

    def visit_CompositeMode(self, node):
        self.visit(node.mode)
        if node.mode.size:
            node.size = node.mode.size
        node.raw_type = node.mode.raw_type
        if hasattr(node.mode, "array_type"):
            node.array_type = node.mode.array_type

    def visit_StringMode(self, node):
        self.visit(node.length)
        if (node.length.raw_type.true_type) != 'const_int' :
            error(node.lineno, "String length '{}' value is not a constant integer expression".format(node.length))
        node.raw_type = self.environment.root["string"]
        node.size = node.length.value
        node.sizeArray = [ 1, node.length.value ]
        # node.array_type = self.environment.root["char"]

    def visit_ArrayMode(self, node):
        node.raw_type = self.environment.root["array"]
        self.visit(node.element_mode)
        node.array_type = node.element_mode.raw_type
        self.visit(node.index_mode_list)
        node.sizeArray = []
        size = node.element_mode.size
        node.sizeArray.append(size)
        for mode in node.index_mode_list:
            size = size * mode.size
            node.sizeArray.append(size)
        node.size = size


    def visit_ArrayElement(self, node):
        self.visit(node.location)
        if node.location._node.raw_type.type == "string":
            node.raw_type = self.environment.root["char"]
            node.array_type = self.environment.root["char"]
            error(node.lineno, "Cannot access string ")
        else:
            node.raw_type = node.location._node.array_type
            node.array_type = node.location._node.array_type
        if hasattr(node.location, "_node"):
            node._node = node.location._node
        for expression in node.expression_list:
            self.visit(expression)
            if expression.raw_type.type != 'int':
                error(node.lineno, "Index value is not a integer expression")


    def visit_ModeName(self, node):
        self.visit(node.type)
        mode = self.environment.lookup(node.type.identifier)
        if( hasattr(mode, "mode") ):
            mode = mode.mode

        if mode is None:
            error(node.lineno, "Mode '{}' not defined".format(node.type.identifier))
            node.size = 1
        else:
            node.size = mode.size
            if hasattr(node.type._node, "array_type"):
                node.array_type = node.type._node.array_type

        node.mode = mode
        node.raw_type = node.type.raw_type

    def visit_AssigmentAction(self, node):
        self.visit(node.location)
        self.visit(node.expression)
        loct_type = node.location.raw_type
        # if hasattr(node.location, "array_type") and loct_type.type != "ref":
        #         loct_type = node.location.array_type
        if loct_type.true_type == 'array' and node.location.array_type.type == "char":
                loct_type = self.environment.root["string"]

        expr_type = node.expression.raw_type
        node.raw_type = node.location.raw_type
        if 'const' in repr(loct_type.true_type) :
            error(node.lineno, "Cannot assign '{}' expression to '{}' type".format(expr_type.type,loct_type.true_type))

        if loct_type.type == expr_type.type:
            if loct_type.type == 'ref' and (node.location.array_type.type != node.expression.array_type.type):
                error(node.lineno, "Cannot assign '{}' ref type to '{}' ref type"
                      .format(node.location.array_type.type, node.expression.array_type.type))
        else:
            error(node.lineno, "Cannot assign '{}' expression to '{}' type".format(expr_type.type,loct_type.type))


        if type(node.location._node).__name__ == "ProcedureDefinition" and \
                not hasattr(node.location._node.returns.mode, "loc"):
            error(node.lineno, "Cannot use non loc value as a variable.")
            sys.exit(1)
            return

        if node.assigning_operator.operator is not None:
            self.raw_type_binary(node, node.assigning_operator.operator, node.location, node.expression)
                                
    def visit_Expression(self, node):
        self.visit(node.value)
        node.raw_type = node.value.raw_type
        if hasattr(node.value, "array_type"):
            node.array_type = node.value.array_type
        if node.raw_type.true_type == "const_int":
            node.calculatedValue = node.value.calculatedValue

    def visit_ConditionalExpression(self, node):
        self.visit(node.boolean_expression)
        self.visit(node.then_expression)
        self.visit(node.elsif_expression)
        self.visit(node.else_expression)
        if node.boolean_expression.raw_type.true_type != self.environment.root["bool"].true_type:
            error(node.lineno, "Should have a boolean clausule on if")
        if not (node.then_expression.raw_type.type == node.else_expression.raw_type.type):
            error(node.lineno, "Conflicting types on conditional expression")
        node.raw_type = node.then_expression.raw_type
        if hasattr(node.then_expression, "array_type"):
                node.array_type = node.then_expression.array_type

    def visit_ElsifExpression(self, node):
        self.visit(node.boolean_expression)
        self.visit(node.then_expression)
        if node.boolean_expression.raw_type.true_type != self.environment.root["bool"].true_type:
            error(node.lineno, "Should have a boolean clausule on if")
        if hasattr(node.then_expression, "array_type"):
                node.array_type = node.then_expression.array_type
        node.raw_type = node.then_expression.raw_type

    def visit_ConditionalClause(self, node):
        self.visit(node.boolean_expression)
        for stmt in node.then_clause:
            if hasattr(node, "returnLocation"):
                stmt.returnLocation = node.returnLocation
                stmt.returnNode = node.returnNode
                stmt.functionName = node.functionName
            self.visit(stmt)

        if node.else_clause is not None:
            for stmt in node.else_clause:
                if hasattr(node, "returnLocation"):
                    stmt.returnLocation = node.returnLocation
                    stmt.returnNode = node.returnNode
                    stmt.functionName = node.functionName
                self.visit(stmt)

        if node.boolean_expression.raw_type.true_type != self.environment.root["bool"].true_type:
            error(node.lineno, "Should have a boolean clausule on if")

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
            if node.operand0.raw_type.true_type == "const_int":
                node.calculatedValue = eval("{} {} {} ".format(node.operand0.calculatedValue,
                                                               node.operation,
                                                               node.operand1.calculatedValue ))
        elif 'const' in node.operand0.raw_type.true_type:
            node.raw_type = node.operand1.raw_type
        elif 'const' in node.operand1.raw_type.true_type:
            node.raw_type = node.operand0.raw_type


    def visit_MonadicOperation(self, node):
        self.visit(node.operand)
        node.raw_type = self.raw_type_unary(node, node.operation, node.operand)
        if node.raw_type.true_type == 'const_int':
            node.calculatedValue = eval("{}{}".format(node.operation,node.operand.calculatedValue))

    def visit_Operand(self, node):
        self.visit(node.value)
        node.raw_type = node.value.raw_type
        if node.raw_type.true_type == 'const_int':
            node.calculatedValue = node.value.calculatedValue
        if hasattr(node.value, "array_type"):
            node.array_type = node.value.array_type

    def visit_CallAction(self, node):
        self.visit(node.call)
        node.raw_type = node.call.raw_type
        if hasattr(node.call, "_node"):
            node._node = node.call._node
        if hasattr(node.call, "array_type"):
            node.array_type = node.call.array_type

    def visit_ProcedureCall(self, node):
        node._node = self.environment.lookup(node.name)
        if node._node is None:
            error(node.lineno, "Call to undefined function '{}'".format(node.name))
            node.raw_type = self.environment.root["void"]
            return
        else:
            node.raw_type = node._node.raw_type
            if hasattr(node._node, "array_type"):
                node.array_type = node._node.array_type
        funcParameters = self.environment.functionsParameters[node.name]
        # VERIFICA QUANTIDADE DE PARAMETROS
        if node.parameters is None:
            node.parameters = []
        if len(node.parameters) != len(funcParameters):
            error(node.lineno, "Wrong call to '{}'. Expected '{}' parameters, got '{}'".format(node.name, len(funcParameters), len(node.parameters)))
            return
        # VERIFICA TIPOS DOS PARAMETROS
        for index, parameter in enumerate(node.parameters):
            self.visit(parameter)
            if parameter.raw_type.type != funcParameters[index].raw_type.type:
                error(node.lineno,
                      "Wrong call to '{}'. Expected '{}' parameter, got '{}' on parameter number {}"
                      .format(node.name, funcParameters[index].raw_type.type, parameter.raw_type.type, index))
            # Verifica se passou uma variavel, e nao uma expressao inteira
            parameter.funcParameter = funcParameters[index]
            if hasattr(funcParameters[index], "loc"):
                if parameter.value.__class__.__name__ != "Operand" or \
                   parameter.value.value.__class__.__name__ != "Location" or \
                   parameter.value.value.location.__class__.__name__ != "Identifier":
                    error(node.lineno, "Wrong call to '{}'. Expected variable, because of loc.".format(node.name))

    def visit_BuiltinCall(self, node):
        node.raw_type = self.environment.root[node.name]
        for parameter in node.parameters:
            self.visit(parameter)

    def visit_StepEnumeration(self, node):
        self.visit(node.loop_counter)
        self.visit(node.start_value)
        self.visit(node.step_value)
        self.visit(node.end_value)
        counter_type = node.loop_counter.raw_type.type
        if self.environment.find(node.loop_counter.identifier) == None :
            error(node.lineno, "Identifier '{}' not defined".format(node.loop_counter.identifier))
        if counter_type != node.start_value.raw_type.type :
            error(node.lineno, "Cannot assign '{}' expression to '{}' type".format(node.start_value.raw_type.type, counter_type))        
        if node.step_value is not None and (counter_type != node.step_value.raw_type.type) :
            error(node.lineno, "Cannot assign '{}' expression to '{}' type".format(node.step_value.raw_type.type, counter_type))        
        if node.end_value is not None and (counter_type != node.end_value.raw_type.type) :
            error(node.lineno, "Cannot compare '{}' expression with '{}' expression".format(node.end_value.raw_type.type, counter_type))     
 
    def visit_RangeEnumeration(self, node):
        self.visit(node.loop_counter)
        self.visit(node.mode)
        counter_type = node.loop_counter.raw_type.type
        if counter_type != node.mode.raw_type.type :            
            error(node.lineno, "Cannot compare '{}' expression with '{}' expression".format(node.loop_counter.raw_type.type, counter_type))     
    
    def visit_DiscreteMode(self, node):
        self.visit(node.mode)
        node.raw_type = node.mode.raw_type

    def visit_ReferenceMode(self, node):
        self.visit(node.mode)
        node.raw_type = self.environment.root["ref"]
        node.array_type = node.mode.raw_type
        node.size = node.mode.size

    def visit_DiscreteRangeMode(self, node):
        self.visit(node.mode)
        self.visit(node.range)
        if node.mode.type != node.range.raw_type.type :
            error(node.lineno, "Range mode and bounds do not have matching types. Mode type is '{}' and bound type is '{}'"
            .format(node.mode.type, node.range.raw_type.type))
        node.raw_type = node.mode.raw_type
    
    def visit_Range(self, node):
        self.visit(node.lower)
        self.visit(node.upper)
        lower_type = node.lower.raw_type.type
        upper_type = node.upper.raw_type.type 
        if  lower_type != upper_type :
            error(node.lineno, "Range bounds do not have matching types. Bound types are '{}' and '{}'".format(lower_type, upper_type))
        if ('const' not in repr(node.lower.raw_type.true_type)) or ('const' not in repr(node.lower.raw_type.true_type)) :
            error(node.lineno, "Range bounds must be constant value expressions")
        node.raw_type = node.lower.raw_type
        node.size = (node.upper.calculatedValue - node.lower.calculatedValue) + 1
        
    def visit_ActionStatement(self, node):
        if (node.identifier is not None):
            if (self.environment.find(node.identifier.identifier) != None) :
                error(node.lineno, "Duplicate definition of label '{}' on same scope".format(node.identifier.identifier))
            node.raw_type = self.environment.root["void"]
            self.environment.add_local(node.identifier.identifier, node)

        if hasattr(node, "returnLocation"):
            node.action.returnLocation = node.returnLocation
            node.action.returnNode = node.returnNode
            node.action.functionName = node.functionName
        self.visit(node.action)              
    def visit_ExitAction(self, node):
        if (self.environment.find(node.call.identifier) == None):
            error(node.lineno, "Unkown label '{}'".format(node.call.identifier))

    def visit_StringSlice(self, node):
        self.visit(node.location)
        self.visit(node.left)
        self.visit(node.right)
        if node.left.raw_type.type != 'int' :
            error(node.lineno, "Index value is not a integer expression")
        if node.right.raw_type.type != 'int' :
            error(node.lineno, "Index value is not a integer expression")
            
    def visit_WhileControl(self, node):
        self.visit(node.expression)
        if node.expression.raw_type.true_type != self.environment.root["bool"].true_type:
            error(node.lineno, "Should have a boolean clausule on while")

