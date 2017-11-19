#
# Copyright 2016 Michael Sparks
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
    elif isinstance(node, list) or isinstance(node, dict) or isinstance(node, str) or isinstance(node, int) or isinstance(node, float) or isinstance(node, bool):
        return node
    return ValueError("Don't know what to do with this value"+repr(node))

class iiNode:
    def __json__():
        raise Exception("No __json__ method defined in this class")

def mkProgram( name, includes, identifiers, statements):

    includes = includes[:]         # Create shallow clone of includes

    program = {}
    program["name"] = name
    program["includes"] = sorted(includes)
    program["main"] = {}

    program["main"]["c_frame"] = {}
    program["main"]["c_frame"]["identifiers"] = identifiers
    program["main"]["c_frame"]["statements"] = statements

    print("PROGRAM", program)
    result = {"PROGRAM" : program }

    return result


def mkOperator(operator):
    if operator=="op_plus":
        return mkOpPlus()

    if operator=="op_minus":
        return mkOpMinus()

    if operator=="op_times":
        return mkOpMultiply()

    if operator=="op_divide":
        return mkOpDivide()

    if operator=="or_operator":
        return mkOpBooleanOr()

    if operator=="and_operator":
        return mkOpBooleanAnd()

    if operator=="not_operator":
        return mkOpBooleanNot()

    raise ValueError("Cannot represent operator", repr(func))

def mkOpPlus():
    return ["op", "plus"]

def mkOpMinus():
    return ["op", "minus"]

def mkOpMultiply():
    return ["op", "times"]

def mkOpDivide():
    return ["op", "divide"]

def mkOpBooleanOr():
    return ["op", "boolean_or"]

def mkOpBooleanAnd():
    return ["op", "boolean_and"]

def mkOpBooleanNot():
    return ["op", "boolean_not"]


def mkAssignment(lvalue, assignment_op, rvalue):
    return ["assignment", lvalue, assignment_op, rvalue]


def mkFunctionCall(func_object, args):
    return ["function_call", func_object, args]


def mkAttributeAccess(expression, attribute):
    return ["attributeaccess", expression, attribute]


def mkIdentifier(identifier):
    return ["identifier", identifier]


def mkString(the_string):
    return ["string", the_string]


def mkInteger(the_integer):
    return ["integer", the_integer]


def mkFloat(the_float):
    return ["double", the_float]


def mkBoolean(the_boolean):
    return ["boolean", the_boolean]


def mkComparison(comparator, left, right):
    return ["op", comparator, left, right]


def mkPrintStatement(args):
    return ["print_statement"] + cargs


def mkWhileStatement(condition, statements):
    return ["while_statement", condition] + statements


def mkIterator(expression):
    return ["iterator", expression]


def mkForStatement(lvalue, iterator, statements, for_statement_PyNode):
    return ["for_statement", lvalue, iterator, statements, for_statement_PyNode]


def mkDefStatement(name, params, block, def_statement_PyNode):
    return ["func_defintion", name, params, block, repr(def_statement_PyNode) ]


def mkPassStatement():
    return ["pass_statement"]


def mkBreakStatement():
    return ["break_statement"]


def mkContinueStatement():
    return ["continue_statement"]


def mkExpressionStatement(expression):
    return ["expression_statement", expression]


def mkIdentifierDeclaration(name, value_type):
    return ["identifier", value_type, name]


def mkElifClause(condition, statements, extended_clause=None):
    if extended_clause:
        return ["elif_clause", condition, statements, extended_clause]
    else:
        return ["elif_clause", condition, statements]

def mkElseClause(statements):
    return ["else_clause", statements]


def mkIfStatement(condition, statements, extended_clause=None):
    if extended_clause:
        return ["if_statement", condition, statements, extended_clause]
    else:
        return ["if_statement", condition, statements]


