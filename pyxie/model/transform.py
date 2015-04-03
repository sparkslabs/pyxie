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

def get_statements(AST):
    statements = []
    if AST[0] == "program":
        assert AST[1][0] == "statements"
        statements = AST[1][1]
    else:
        print AST[0]
    return statements

def todo(*args):
    print "TODO", " ".join([repr(x) for x in args])

def find_variables(AST):
    variables = {}
    statements = get_statements(AST)
    for statement in statements:
        tag, rest = statement[0], statement[1:]
        if tag == "assignment_statement":
            lvalue, assigntype, rvalue = rest
            if assigntype[1] != "=":
                todo("assignment where the assigntype is not '='")
                continue # Skip
            if lvalue[1] != "IDENTIFIER":
                todo("assignment where the lvalue is not an identifier")
                continue # Skip
            if rvalue[0] != "value_literal":
                todo("assignment where the rvalue is not a value_literal")
                continue # Skip

            identifer = lvalue[0]
            v_type = rvalue[2]
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
    if ptype == "STRING":  return "string"
    if ptype == "NUMBER":  return "int"
    if ptype == "BOOLEAN": return "bool"
    if ptype == "FLOAT":   return "double"
    raise UnknownType("Cannot identify C Type for %s" % ptype)

def includes_for_ctype(ctype):
    if ctype == "string":  return "<string>"

def includes_for_cstatement(cstatement):
    if cstatement[0] == "print_statement": return "<iostream>"

def crepr_literal(pyliteral):
    assert pyliteral[0] == "value_literal"
    ctype = pyliteral[2]
    if ctype == "STRING":
        return '"' + pyliteral[1] + '"'
    if ctype == "NUMBER":
        return repr(pyliteral[1])
    raise ValueError("Do not not know how to create crepr_literal for " + repr(pyliteral))


def convert_assignment(assignment):
    lvalue, assigntype, rvalue = assignment

    if assigntype[1] != "=":
        todo("Convert Assignment where assigntype is not '='")
        raise CannotConvert("Cannot convert assignment where assigntype is not '='")
    if lvalue[1] != "IDENTIFIER":
        todo("assignment where the lvalue is not an identifier")
        raise CannotConvert("Cannot convert assignment where the lvalue is not an identifier")
    if rvalue[0] != "value_literal":
        todo("assignment where the rvalue is not a value_literal")
        raise CannotConvert("Cannot convert assignment where the rvalue is not a value_literal")

    print rvalue
    lvalue = lvalue[0]
    rvalue = crepr_literal(rvalue)
#    rvalue = rvalue[1]
    return ["assignment", lvalue, "=", rvalue ]
#    return ["assignment", lvalue, "=", '"'+rvalue+'"' ]

def convert_print(arg_spec):
    arg_spec = arg_spec[0]
    cstatement = []
    cargs = []
    print "arg_spec",arg_spec[0]
    for arg in arg_spec:
        print arg[0]
        if arg[0] != "value_literal":
            todo("Handle print for non-value-literals")
            raise CannotConvert("Cannot convert print for non-value-literals")
        carg = arg[1]
        cargs.append(carg)
    return ["print_statement"] + cargs

def convert_statements(AST):
    cstatements = []
    statements = get_statements(AST)
    for statement in statements:
        tag, rest = statement[0], statement[1:]
        print tag
        try:
            if tag == "assignment_statement":
                cstatement = convert_assignment(rest)
                print cstatement
                cstatements.append(cstatement)
            print "HERE!?", repr(tag)
            if tag == "print_statement":
                print "Flooble"
                cstatement = convert_print(rest)
                cstatements.append(cstatement)

        except CannotConvert:
            pass
    return cstatements

def ast_to_cst(program_name, AST):
    cst = {}

    # Extract and handle variables
    pvariables = find_variables(AST)
    cvariables = []
    ctypes = {}
    includes = []
    for name in pvariables:
        ctype = python_type_to_c_type(pvariables[name])
        identifier = [ "identifier", ctype, name ]
        cvariables.append(identifier)
        ctypes[ctype] = True

    cstatements = convert_statements(AST)
    print cstatements

    # Based on variables, update includes
    for ctype in ctypes:
        inc = includes_for_ctype(ctype)
        if inc:
            includes.append(inc)

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
    AST =  ['program',
             ['statements',
              [['assignment_statement',
                ['greeting', 'IDENTIFIER', 1],
                ['ASSIGN', '='],
                ['value_literal', 'hello', 'STRING', 1]],
               ['assignment_statement',
                ['name', 'IDENTIFIER', 2],
                ['ASSIGN', '='],
                ['value_literal', 'world', 'STRING', 2]],
               ['print_statement',
                [['value_literal', 'greeting', 'IDENTIFIER', 4],
                 ['value_literal', 'name', 'IDENTIFIER', 4]]]]]]
    expect = {
                 "PROGRAM": {
                     "name": "hello",
                     "includes": [ "<iostream>", "<string>" ],
                     "main": {
                         "c_frame": {
                             "identifiers": [
                                 [ "identifier", "string", "greeting" ],
                                 [ "identifier", "string", "name" ]
                             ],
                             "statements": [
                                 [ "assignment", "greeting", "=", "\"hello\"" ],
                                 [ "assignment", "name", "=", "\"world\"" ],
                                 [ "print_statement", "greeting", "name" ]
                             ]
                         }
                     }
                 }
             }

    actual = ast_to_cst("hello", AST)

    print "actual == expect --->", actual == expect

    import json
    import pprint
    # print json.dumps(actual, indent=4)
    pprint.pprint(actual)

