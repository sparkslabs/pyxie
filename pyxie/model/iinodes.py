#
# Copyright 2017 Michael Sparks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""
This file will contain objects used to represent the independent intermediate
format of the program.

Initially it's being a bridging/extraction point.
"""

def jsonify(node):
    if isinstance(node, iiNode):
        print "here"
        return node.__json__()
    elif ( isinstance(node, list) or isinstance(node, dict) or isinstance(node, str) or isinstance(node, int) or isinstance(node, float) or isinstance(node, bool) ):
        return node
    return ValueError("Don't know what to do with this value"+repr(node))


class iiNode(object): # This is to allow intermediate thunk check whether it has an iiNode or not...
    tag = "iinode"
    def __init__(self):
        raise TypeError("Abstract Base class method called")
    def __json__(self):
        raise TypeError("Abstract Base class method called")

class iiProgram(iiNode):
    tag = "program"
    def __init__(self, name, includes, identifiers, statements):
        self.name = name
        self.includes = includes[:]         # Create shallow clone of includes
        self.global_identifiers = identifiers
        self.statements = statements

    def __json__(self):
        # Backwards compatibility thunk - later will be used for debugging/a pretty printing representation
        program = {}
        program["name"] = self.name
        program["includes"] = sorted(self.includes)
        program["main"] = {}

        program["main"]["c_frame"] = {}
        program["main"]["c_frame"]["identifiers"] = self.global_identifiers
        program["main"]["c_frame"]["statements"] = self.statements
        print("PROGRAM", program)
        result = {"PROGRAM" : program }
        return result

class iiOpNode(iiNode):
    tag = "iiopnode"
    def __init__(self):
        pass

    def __json__(self):
        return ["op", self.tag ]

class iiOpPlus(iiOpNode):
    tag = "plus"

class iiOpMinus(iiOpNode):
    tag = "minus"

class iiOpMultiply(iiOpNode):
    tag = "times"

class iiOpDivide(iiOpNode):
    tag = "divide"

class iiOpBooleanOr(iiOpNode):
    tag = "boolean_or"

class iiOpBooleanAnd(iiOpNode):
    tag = "boolean_and"

class iiOpBooleanNot(iiOpNode):
    tag = "boolean_not"

class iiAssignment(iiNode):
    tag = "assignment"
    def __init__(self, lvalue, assignment_op, rvalue):
        self.lvalue = lvalue
        self.assignment_op = assignment_op
        self.rvalue= rvalue
    def __json__(self):
        return ["assignment", self.lvalue, self.assignment_op, self.rvalue ]



class iiFunctionCall(iiNode):
    tag = "function_call"
    def __init__(self, func_object, args):
        self.iifunc_object = func_object
        self.iifunc_call_args = args

    def __json__(self):
        return ["function_call", self.iifunc_object, self.iifunc_call_args ]


class iiAttributeAccess(iiNode):
    tag = "attributeaccess"
    def __init__(self, expression, attribute):
        self.expression = expression
        self.attribute = attribute

    def __json__(self):
        return ["attributeaccess", self.expression, self.attribute]

class iiIdentifier(iiNode):
    tag = "identifier"
    def __init__(self, identifier):
        self.identifier = identifier

    def __json__(self):
        return ["identifier", self.identifier]


class iiString(iiNode):
    tag = "string"
    def __init__(self, the_string):
        self.the_string = the_string

    def __json__(self):
        return ["string", self.the_string]


class iiInteger(iiNode):
    tag = "integer"
    def __init__(self, the_integer):
        self.the_integer = the_integer

    def __json__(self):
        return ["integer", self.the_integer]




class iiFloat(iiNode):
    tag = "double"
    def __init__(self, the_float):
        self.the_float = the_float

    def __json__(self):
        return ["double", self.the_float]



class iiBoolean(iiNode):
    tag = "boolean"
    def __init__(self, the_boolean):
        self.the_boolean = the_boolean
 
    def __json__(self):
        return ["boolean", self.the_boolean]


class iiComparison(iiNode):
    tag = "op"
    def __init__(self, comparator, left, right):
        self.comparator = comparator
        self.left = left
        self.right = right
    def __json__(self):
        return ["op", self.comparator, self.left, self.right]



class iiWhileStatement(iiNode):
    tag = "while_statement"
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements

    def __json__(self):
        return ["while_statement", self.condition] + self.statements


class iiIterator(iiNode):
    tag = "iterator"
    def __init__(self, expression):
        self.expression = expression

    def __json__(self):
        return ["iterator", self.expression]


class iiForStatement(iiNode):
    tag = "for_statement"
    def __init__(self, lvalue, iterator, statements, for_statement_PyNode):
        self.lvalue = lvalue
        self.iterator = iterator
        self.statements = statements
        self.for_statement_PyNode = for_statement_PyNode

    def __json__(self):
        return ["for_statement", self.lvalue, self.iterator, self.statements, self.for_statement_PyNode]

class iiDefStatement(iiNode):
    tag = "func_defintion"
    def __init__(self, name, params, block, def_statement_PyNode):
        self.name = name
        self.params = params
        self.block = block
        self.def_statement_PyNode = def_statement_PyNode

    def __json__(self):
        return ["func_defintion", self.name, self.params, self.block, repr(self.def_statement_PyNode) ]



class iiPassStatement(iiNode):
    tag = "pass_statement"
    def __init__(self):
        pass

    def __json__(self):
        return ["pass_statement"]


class iiBreakStatement(iiNode):
    tag = "break_statement"
    def __init__(self):
        pass
    def __json__(self):
        return ["break_statement"]

class iiContinueStatement(iiNode):
    tag = "continue_statement"
    def __init__(self):
        pass

    def __json__(self):
        return ["continue_statement"]

class iiExpressionStatement(iiNode):
    tag = "expression_statement"
    def __init__(self, expression):
        self.expression = expression

    def __json__(self):
        return ["expression_statement", self.expression]



class iiIdentifierDeclaration(iiNode):
    tag = "identifier"
    def __init__(self, name, value_type):
        self.value_type = value_type
        self.name = name

    def __json__(self):
        return ["identifier", self.value_type, self.name]

class iiElifClause(iiNode):
    tag = "elif_clause"
    def __init__(self, condition, statements, extended_clause=None):
        self.condition = condition
        self.statements = statements
        self.extended_clause = extended_clause

    def __json__(self):
        if self.extended_clause:
            return ["elif_clause", self.condition, self.statements, self.extended_clause]
        else:
            return ["elif_clause", self.condition, self.statements]


class iiElseClause(iiNode):
    tag = "else_clause"
    def __init__(self, statements ):
        self.statements = statements

    def __json__(self):
        return ["else_clause", self.statements]


class iiIfStatement(iiNode):
    tag = "if_statement"
    def __init__(self, condition, statements, extended_clause=None):
        self.condition = condition
        self.statements = statements
        self.extended_clause = extended_clause

    def __json__(self):
        if self.extended_clause:
            return ["if_statement", self.condition, self.statements, self.extended_clause]
        else:
            return ["if_statement", self.condition, self.statements]


def mkIfStatement(condition, statements, extended_clause=None):
    return iiIfStatement(condition, statements, extended_clause)

def mkElifClause(condition, statements, extended_clause=None):
    return iiElifClause(condition, statements, extended_clause)

def mkElseClause(statements):
    return iiElseClause(statements)

def mkBreakStatement():
    return iiBreakStatement()

def mkContinueStatement():
    return iiContinueStatement()

def mkExpressionStatement(expression):
    return iiExpressionStatement(expression)

def mkIdentifierDeclaration(name, value_type):
    return iiIdentifierDeclaration(name, value_type)

def mkComparison(comparator, left, right):
    return iiComparison(comparator, left, right)

def mkWhileStatement(condition, statements):
    return iiWhileStatement(condition, statements)


def mkForStatement(lvalue, iterator, statements, for_statement_PyNode):
    return iiForStatement(lvalue, iterator, statements, for_statement_PyNode)

def mkDefStatement(name, params, block, def_statement_PyNode):
    return iiDefStatement(name, params, block, def_statement_PyNode)

def mkPassStatement():
    return iiPassStatement()

def mkAttributeAccess(expression, attribute):
    return iiAttributeAccess(expression, attribute)

def mkIdentifier(identifier):
    return iiIdentifier(identifier)

def mkString(the_string):
    return iiString(the_string)

def mkInteger(the_integer):
    return iiInteger( the_integer)

def mkFloat(the_float):
    return iiFloat(the_float)

def mkBoolean(the_boolean):
    return iiBoolean(the_boolean)

def mkIterator(expression):
    return iiIterator(expression)

def mkOpPlus():
    return iiOpPlus()

def mkOpMinus():
    return iiOpMinus()

def mkOpMultiply():
    return iiOpMultiply()

def mkOpDivide():
    return iiOpDivide()

def mkOpBooleanOr():
    return iiOpBooleanOr()

def mkOpBooleanAnd():
    return iiOpBooleanAnd()

def mkOpBooleanNot():
    return iiOpBooleanNot()

def mkAssignment(lvalue, assignment_op, rvalue):
    return iiAssignment(lvalue, assignment_op, rvalue)

def mkFunctionCall(func_object, args):
    return iiFunctionCall(func_object, args)

def mkOperator(operator):
    result = None
    if operator=="op_plus":
        result = mkOpPlus()

    if operator=="op_minus":
        result = mkOpMinus()

    if operator=="op_times":
        result = mkOpMultiply()

    if operator=="op_divide":
        result = mkOpDivide()

    if operator=="or_operator":
        result = mkOpBooleanOr()

    if operator=="and_operator":
        result = mkOpBooleanAnd()

    if operator=="not_operator":
        result = mkOpBooleanNot()

    if result:
        return result

    raise ValueError("Cannot represent operator", repr(func))

def mkProgram( name, includes, identifiers, statements):
    program = iiProgram(name, includes, identifiers, statements)
    return program
