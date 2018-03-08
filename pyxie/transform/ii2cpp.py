#!/usr/bin/python
#
# Copyright 2018 Michael Sparks
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

# Transform iinodes to cppnodes
# FIXME: WIP

from __future__ import print_function
from __future__ import absolute_import

from pyxie.model.iinodes import ExpressionIsPrintBuiltin

from pyxie.model.cppnodes import CppProgram, \
                                 CppIdentifier, \
                                 CppAssignment, \
                                 CppExpressionStatement, \
                                 CppWhileStatement, \
                                     CppIfStatement

import pyxie.model.cppnodes


def mkProgram(iiprogram):
    program = CppProgram()
    program.name = iiprogram.name
    program.includes = iiprogram.includes

    for identifier in iiprogram.global_identifiers:
        value_type = identifier.value_type
        name = identifier.name
        program.main_cframe.identifiers.append(CppIdentifier(value_type, name))

    for statement in iiprogram.statements:
        conc_statement = mkStatement(statement)
        program.main_cframe.statements.append(conc_statement)

    return program

def mkStatement(statement_spec):
    ss = statement_spec
    statement_type = statement_spec.tag
    if statement_type == "assignment":
        s = statement_spec
        return CppAssignment( s.lvalue, s.rvalue, s.assignment_op)

    elif statement_type == "expression_statement":
        expression = statement_spec.expression
        if expression.tag == "function_call":
            if ExpressionIsPrintBuiltin(expression):
                print("XXXX", expression)
                args = expression.iifunc_call_args
                return CppPrintStatement(args)
        return CppExpressionStatement(expression)

    elif statement_type == "while_statement":
        return CppWhileStatement(statement_spec.condition, *statement_spec.statements)

    elif statement_type == "for_statement":
        s = statement_spec
        return CppForStatement(s.lvalue,
                               s.iterator,
                               s.statements,
                               s.for_statement_PyNode)

    elif statement_type == "if_statement":
        if ss.extended_clause == None:
            return CppIfStatement(ss.condition, ss.statements)
        else:
            return CppIfStatement(ss.condition, ss.statements, ss.extended_clause)

    elif statement_type == "pass_statement":
        return CppEmptyStatement()

    elif statement_type == "break_statement":
        return CppBreakStatement()

    elif statement_type == "continue_statement":
        return CppContinueStatement()

    else:
        print("Unknown statement type", statement_type, ss)
        raise Exception("Unhandlable statement type: ", statement_type)

def iioperator_to_cpp_repr(iioperator): # FIXME: Terrible name

    # Converts an iiNode representation of an operator
    op_type = iioperator.operator

    print("ARG", iioperator, op_type)
    if op_type == "plus": return "+"
    if op_type == "minus": return "-"
    if op_type == "times": return "*"
    if op_type == "divide": return "/"
    if op_type == "boolean_or": return " || "
    if op_type == "boolean_and": return " && "
    if op_type == "boolean_not": return " ! "

    if op_type in ["<", ">", "==", ">=", "<=", "!="]:
        return op_type

    if op_type == "<>": return "!="

    return TypeError("Cannot convert operator", iioperator, op_type)


# FIXME: These are indicative of a problem.

pyxie.model.cppnodes.mkStatement = mkStatement
pyxie.model.cppnodes.iioperator_to_cpp_repr = iioperator_to_cpp_repr


if __name__ == "__main__":
    pass