#!/usr/bin/python
#
# Copyright 2015 Michael Sparks
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

# This is currently working from the AST as represented by lists,
# switching to intermediate lists and then to nodes.

from pyxie.model.pynode import jdump
import pyxie.model.pynode as nodes

def todo(*args):
    print "TODO", " ".join([repr(x) for x in args])

# Assumes that the analysis phase has taken place
def find_variables(AST):
    variables = {}
    for node in AST.depth_walk():
        if node.tag == "assignment_statement":
            if node.assign_type != "=":
                todo("find_variables - assignment where the assign_type is not '='")
                continue # Skip
            if node.lvalue.tag != "identifier":
                todo("find_variables - assignment where the lvalue is not an identifier")
                continue # Skip

            lvalue, rvalue, assign_type = node.lvalue, node.rvalue, node.assign_type
            identifer = lvalue.value
            v_type = lvalue.ntype

            if identifer in variables:
                todo("we could check that the identifier doesn't change type")
                continue # Skip
            variables[identifer] = v_type

    return variables

class UnknownType(Exception):
    pass

class CannotConvert(Exception):
    pass

def python_type_to_c_type(ptype):
    if ptype == "string":  return "string"
    if ptype == "integer":  return "int"
    if ptype == "bool": return "bool"
    if ptype == "float":   return "double"
    if ptype == "char": return "char"
    raise UnknownType("Cannot identify C Type for %s" % ptype)

def includes_for_ctype(ctype):
    if ctype == "string":  return "<string>"

def includes_for_cstatement(cstatement):
    if cstatement[0] == "print_statement": return "<iostream>"

def crepr_literal(pyliteral):
    assert isinstance(pyliteral, nodes.PyValueLiteral)

    ptype = pyliteral.get_type()
    ctype = python_type_to_c_type(ptype)

    if ctype == "string":
        result = pyliteral.value
        result = result.replace('"','\\"')
        return '"' + result + '"'

    if ctype == "char":
        char = pyliteral.value
        char = char.replace("'","\\'")
        return "'" + char + "'"

    if ctype == "int":
        return repr(pyliteral.value)

    if ctype == "double":
        return repr(pyliteral.value)

    if ctype == "bool":
        if pyliteral.value:
            return "true"
        else:
            return "false"


    raise ValueError("Do not not know how to create crepr_literal for " + repr(pyliteral))

def crepr_op(py_op):
    assert isinstance(py_op, nodes.PyOperator)
#    assert py_op[0] == "operator_function"
    func = py_op.tag

    if func == "op_plus":
        return ["op", "plus"]
    if func == "op_minus":
        return ["op", "minus"]
    if func == "op_times":
        return ["op", "times"]
    if func == "op_divide":
        return ["op", "divide"]
    else:
        todo("Cannot yet convert operators functions other than plus...")
        raise CannotConvert("Cannot yet convert operators functions other than plus...:" + repr(py_op))

def convert_assignment(assignment):
    lvalue, assign_type, rvalue = assignment.lvalue,assignment.assign_type, assignment.rvalue

    if assign_type != "=":
        todo("Convert Assignment where assign_type is not '='")
        raise CannotConvert("Cannot convert assignment where assign_type is not '='")

    if lvalue.tag != "identifier":
        todo("assignment where the lvalue is not an identifier")
        raise CannotConvert("Cannot convert assignment where the lvalue is not an identifier")

    if not ( isinstance(assignment.rvalue, nodes.PyOperator) or
             isinstance(assignment.rvalue, nodes.PyValueLiteral) ) :

        todo("assignment where the rvalue is not a value_literal or operator")
        raise CannotConvert("Cannot convert assignment where the rvalue is not a value_literal")

    # print rvalue
    clvalue = lvalue.value # FIXME: This is only valid for identifiers
    if isinstance(assignment.rvalue, nodes.PyValueLiteral):
        crvalue = crepr_literal(rvalue)

    if isinstance(assignment.rvalue, nodes.PyOperator):
        crvalue = convert_operator_function(rvalue)

    return ["assignment", clvalue, "=", crvalue ]

def convert_value_literal(arg):
    # print repr(arg), arg
    stype = None
    tag, value, vtype, line = arg.tag, arg.value,arg.get_type(), arg.lineno
    if tag == "identifier":
        return ["identifier",  value]

    if vtype == "string":
        return ["string",  value]
    if vtype == "integer":
        return ["integer",  value]
    if vtype == "float":
        return ["double",  value]
    if vtype == "bool":
        if value == True:
            value = "true"
        else:
            value = "false"
        return ["boolean",  value]

    todo("CONVERSION: Cannot handle other value literals %s" % repr(arg))
    todo("CONVERSION: %s %s %s %d" % (tag, repr(value), repr(vtype), line))
    raise CannotConvert("Cannot convert value-literal of type" + repr(arg))


def convert_operator_function(opfunc):
    print "CONVERT - convert_operator_function", repr(opfunc)
    assert isinstance(opfunc, nodes.PyOperator)
#    assert opfunc[0] == "operator_function"

    func = opfunc.tag
    arg1 = opfunc.arg1
    arg2 = opfunc.arg2

    crepr_arg1 = convert_arg(arg1)
    crepr_arg2 = convert_arg(arg2)
    print "crepr_arg1", repr(crepr_arg1)
    print "crepr_arg2", repr(crepr_arg2)

    result = crepr_op(opfunc) + [crepr_arg1, crepr_arg2]
    print repr(result)
    return result

    #todo("Cannot yet convert operator functions")
    #raise CannotConvert("Cannot convert operator function :" + repr(arg))


def convert_arg(arg):
    if isinstance(arg, nodes.PyValueLiteral):
        print "CONVERTING LITERAL", arg
        return convert_value_literal(arg)
    elif isinstance(arg, nodes.PyOperator):
        return convert_operator_function(arg)
    elif isinstance(arg, nodes.PyFunctionCall):
        print "NEED TO CONVERT FUNCTION CALL TO SOMETHING THE C CODE GENERATOR CAN HANDLE"
        cargs = []
        for expr in arg.expr_list:
            #print arg
            #print "We need to convert the arg", arg
            crepr = convert_arg(expr)
            carg = crepr
            cargs.append(carg)

        return ["function_call", convert_value_literal(arg.identifier),  cargs ]
        return ["Nothing"]
#        return convert_operator_function(arg)
    else:
        todo("Handle print for non-value-literals")
        raise CannotConvert("Cannot convert print for non-value-literals")

def convert_print(print_statement):
    cstatement = []
    cargs = []
    for arg in print_statement.expr_list:
        #print arg
        #print "We need to convert the arg", arg
        crepr = convert_arg(arg)
        carg = crepr
        cargs.append(carg)
    return ["print_statement"] + cargs

def convert_expression_statement(statement):
    print "CONVERTING EXPRESSION STATEMENTS", statement.value
    print "EXPRESSION STATEMENT", statement.value.tag
    crepr = convert_arg(statement.value)
    print "RECHED HERE"
    print "CONVERTED ", crepr
    return ["expression_statement", crepr]

def convert_statements(AST):
    cstatements = []
    statements = AST.statements
    for statement in statements:
        try:
            if statement.tag == "assignment_statement":
                cstatement = convert_assignment(statement)
                print cstatement
                cstatements.append(cstatement)
            elif statement.tag == "print_statement":
                cstatement = convert_print(statement)
                cstatements.append(cstatement)
            elif statement.tag == "expression_statement":
                cstatement = convert_expression_statement(statement)
                cstatements.append(cstatement)
            else:
                print "SKIPPING STATEMENT", statement.tag

        except CannotConvert:
            print "REACHED HERE FOR", statement
            pass
    return cstatements

def ast_to_cst(program_name, AST):
    cst = {}

    ast_includes = [ x.replace("#include ","") for x in AST.includes ]
    print "AST.includes = ", ast_includes
    # Extract and handle variables
    pvariables = find_variables(AST)
    cvariables = []
    ctypes = {}
    # includes = []
    includes = [ x.replace("#include ","") for x in AST.includes ]
    names = pvariables.keys()
    names.sort()
    for name in names:
        ctype = python_type_to_c_type(pvariables[name])
        identifier = [ "identifier", ctype, name ]
        cvariables.append(identifier)
        ctypes[ctype] = True

    print "cvariables",cvariables

    cstatements = convert_statements(AST)
    print cstatements

    # Based on variables, update includes
    for ctype in ctypes:
        inc = includes_for_ctype(ctype)
        if inc:
            includes.append(inc)

    print "INCLUDES::", includes
    # Based on statements, update includes
    for cstatement in cstatements:
        inc = includes_for_cstatement(cstatement)
        if inc:
            includes.append(inc)

    program = {}
    program["name"] = program_name
    program["includes"] = sorted(includes)
    program["main"] = {}
    program["main"]["c_frame"] = {}
    program["main"]["c_frame"]["identifiers"] = cvariables
    program["main"]["c_frame"]["statements"] = cstatements

    return { "PROGRAM" : program }


if __name__ == "__main__":
    AST =   ['program',
             ['statements',
              [['assignment_statement',
                ['first', 'IDENTIFIER', 1],
                ['ASSIGN', '='],
                ['value_literal', 1, 'NUMBER', 'INT', 1]],
               ['assignment_statement',
                ['second', 'IDENTIFIER', 2],
                ['ASSIGN', '='],
                ['value_literal', 2, 'NUMBER', 'INT', 2]],
               ['assignment_statement',
                ['third', 'IDENTIFIER', 3],
                ['ASSIGN', '='],
                ['value_literal', 3, 'NUMBER', 'INT', 3]],
               ['print_statement',
                [['value_literal', 'first', 'IDENTIFIER', 5],
                 ['value_literal', 'second', 'IDENTIFIER', 5],
                 ['value_literal', 'third', 'IDENTIFIER', 5]]],
               ['print_statement',
                [['value_literal', 1, 'NUMBER', 'INT', 6],
                 ['value_literal', 2, 'NUMBER', 'INT', 6],
                 ['value_literal', 'hello', 'STRING', 6]]]]]]

    expect = {
        'PROGRAM': {'includes': ['<iostream>', '<iostream>'],
             'main': {'c_frame': {'identifiers': [['identifier', 'int', 'second'],
                                                  ['identifier', 'int', 'third'],
                                                  ['identifier', 'int', 'first']],
                                  'statements': [['assignment', 'first', '=', '1'],
                                                 ['assignment', 'second', '=', '2'],
                                                 ['assignment', 'third', '=', '3'],
                                                 ['print_statement',
                                                      ['identifier', 'first'],
                                                      ['identifier', 'second'],
                                                      ['identifier', 'third']],
                                                 ['print_statement',
                                                      ["integer", 1],
                                                      ["integer", 2],
                                                      ["string", 'hello']]]}},
             'name': 'hello_world_mixed'}}

    AST = ['program',
           ['statements',
            [['print_statement',
              [['operator_function',
                'plus',
                ['value_literal', 1, 'NUMBER', 'INT', 1],
                ['value_literal', 1, 'NUMBER', 'INT', 1]]]]]]]

    expect = {
        'PROGRAM': {'includes': ['<iostream>'],
             'main': {'c_frame': {'identifiers': [],
                                  'statements': [['print_statement', ['op', 'plus', 
                                                                            ["integer", 1],
                                                                            ["integer", 1]]]
,
                                                ] }},
             'name': 'hello_operators'}}


    actual = ast_to_cst("hello_operators", AST)

    print "actual == expect --->", actual == expect

    import json
    import pprint
    # print json.dumps(actual, indent=4)
    pprint.pprint(actual)
    pprint.pprint(expect)

