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

# This is currently working from the AST as represented by lists,
# switching to intermediate lists and then to nodes.

from __future__ import print_function
from __future__ import absolute_import

import pprint

from pyxie.model.pynode import jdump
import pyxie.model.pynode as nodes
from pyxie.model.pynode import depth_walk
from pyxie.model.functions import builtins
from pyxie.model.functions import profile_types

from pyxie.model.iinodes import *

iterator_unique_base = 0

trace = False

def DebugPrint(*args):
    if trace:
        print(*args)

class UnknownType(Exception):
    pass

class CannotConvert(Exception):
    pass

#
# Support code to cover intermediate stages of conversion
#
def statement_type(iistatement):
    statementType = iistatement.tag
    return statementType



def todo(*args):
    print("TODO", " ".join([repr(x) for x in args]))

#
# Assumes that the analysis phase has taken place
# TODO: This should really be able to delve inside the context that's been created during analysis
#
def find_variables(AST):
    global iterator_unique_base
    variables = {}
    for node in depth_walk(AST):
        if node.tag == "for_statement":
            for_statement = node
            lvalue = for_statement.identifier
            rvalue_source = for_statement.expression
            identifier = lvalue.value
            v_type = lvalue.ntype
            DebugPrint("FOR LOOP, IDENTIFIER", identifier, "HAS TYPE", v_type)
            variables[identifier] = v_type
            if for_statement.expression.isiterator:
                DebugPrint("#####################################################")
                DebugPrint("Extracting generator intermediate variable")
                DebugPrint(for_statement.expression)
                if isinstance(for_statement.expression, nodes.PyFunctionCall):
                    identifier = for_statement.expression.func_label             # FIXME: May not be an identifier...
                    DebugPrint("Bibble", identifier)
                    DebugPrint("Bibble", identifier.value)
                    iterator_type = identifier.value
                    iterator_unique_base += 1
                    iterator_name = identifier.value + "_iter_" + str(iterator_unique_base)
                    DebugPrint("iterator_type", iterator_type)
                    DebugPrint("iterator_name", iterator_name)
                    variables[iterator_name] = iterator_type
                    for_statement.expression.ivalue_name = iterator_name

                DebugPrint("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

        if node.tag == "assignment_statement":
            if node.assign_type != "=":
                todo("find_variables - assignment where the assign_type is not '='")
                continue # Skip
            if node.lvalue.tag != "identifier":
                todo("find_variables - assignment where the lvalue is not an identifier")
                continue # Skip

            lvalue, rvalue, assign_type = node.lvalue, node.rvalue, node.assign_type
            identifier = lvalue.value
            v_type = lvalue.ntype

            if identifier in variables:
                todo("we could check that the identifier doesn't change type")
                continue # Skip
            variables[identifier] = v_type

    return variables


def python_type_to_c_type(ptype):
    if ptype == "string": return "string"
    if ptype == "integer": return "int"

    if ptype == "signedlong": return "long"
    if ptype == "unsignedlong": return "unsigned long"

    if ptype == "bool": return "bool"
    if ptype == "float": return "double"
    if ptype == "char": return "char"

    if ptype in builtins: return ptype

    if ptype in profile_types: return ptype

    raise UnknownType("Cannot identify C Type for %s" % ptype)

def includes_for_ctype(ctype):
    if ctype == "string": return "<string>"


def includes_for_iistatement(iistatement):
    if statement_type(iistatement) == "print_statement": return "<iostream>"

def crepr_literal(pyliteral):
    assert isinstance(pyliteral, nodes.PyValueLiteral)

    ptype = pyliteral.get_type()
    ctype = python_type_to_c_type(ptype)

    if ctype == "string":
        result = pyliteral.value
        result = result.replace('"', '\\"')
        return '"' + result + '"'

    if ctype == "char":
        char = pyliteral.value
        char = char.replace("'", "\\'")
        return "'" + char + "'"

    if ctype == "int":
        return repr(pyliteral.value)

    if ctype == "long":
        return repr(pyliteral.value)

    if ctype == "unsigned long":
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
    assert isinstance(py_op, nodes.PyOperator) or isinstance(py_op, nodes.PyBoolOperator)

    args = py_op.args()
    crepr_args = [ convert_arg(x) for x in args ]

    try:
        result = iiOperator(py_op.tag, crepr_args)
    except ValueError:
        raise CannotConvert("Cannot represent operator", py_op.tag)
    return result


def convert_assignment(assignment):
    lvalue, assign_type, rvalue = assignment.lvalue, assignment.assign_type, assignment.rvalue

    if assign_type != "=":
        todo("Convert Assignment where assign_type is not '='")
        raise CannotConvert("Cannot convert assignment where assign_type is not '='")

    if lvalue.tag != "identifier":
        todo("assignment where the lvalue is not an identifier")
        raise CannotConvert("Cannot convert assignment where the lvalue is not an identifier")

    if not (isinstance(assignment.rvalue, nodes.PyOperator) or
            isinstance(assignment.rvalue, nodes.PyValueLiteral) or
            isinstance(assignment.rvalue, nodes.PyComparisonOperator) or
            isinstance(assignment.rvalue, nodes.PyBoolOperator) or
            isinstance(assignment.rvalue, nodes.PyFunctionCall)):

        todo("assignment where the rvalue is not a value_literal, operator, or function call")
        raise CannotConvert("Cannot convert assignment where the rvalue is not a value_literal, operator, or function call")

    # DebugPrint(rvalue)
    clvalue = lvalue.value # FIXME: This is only valid for identifiers

    # If the rvalue is a PyIdentifier, it should pass through as the identifier
    if isinstance(assignment.rvalue, nodes.PyIdentifier):
        crvalue = rvalue.value

    elif isinstance(assignment.rvalue, nodes.PyValueLiteral):
        DebugPrint("nodes.PyValueLiteral", assignment.rvalue)
        crvalue = crepr_literal(rvalue)

    elif isinstance(assignment.rvalue, nodes.PyOperator):
        crvalue = convert_operator_function(rvalue)

    elif isinstance(assignment.rvalue, nodes.PyBoolOperator):
        crvalue = convert_bool_operator_function(rvalue)

    elif isinstance(assignment.rvalue, nodes.PyComparisonOperator):
        crvalue = convert_comparison(rvalue)

    elif isinstance(assignment.rvalue, nodes.PyFunctionCall):
        arg = assignment.rvalue
        DebugPrint("NEED TO CONVERT FUNCTION CALL TO SOMETHING THE C CODE GENERATOR CAN HANDLE")
        cargs = []
        if arg.expr_list:
            for expr in arg.expr_list:
                crepr = convert_arg(expr)
                carg = crepr
                cargs.append(carg)

        func_label = convert_value_literal(arg.func_label)  # FIXME: func_label may not be an identifier...
        crvalue = iiFunctionCall(func_object=func_label, args=cargs)

    result = iiAssignment(lvalue=clvalue, assignment_op="=", rvalue=crvalue)
    return result


def convert_value_literal(arg):
    # DebugPrint(repr(arg), arg)
    stype = None
    DebugPrint ("ARG::", arg.tag)

    if arg.tag == "attributeaccess":
        expression = convert_value_literal(arg.expression)
        attribute = convert_value_literal(arg.attribute)

        return iiAttributeAccess(expression, attribute)

    if arg.tag == "attribute":
        x = convert_value_literal(arg.value)
        return x

    tag, value, vtype, line = arg.tag, arg.value, arg.get_type(), arg.lineno

    if tag == "identifier":
        return iiIdentifier(identifier=value)

    if vtype == "string":
        return iiString(the_string=value)

    if vtype == "integer":
        return iiInteger(the_integer=value)

    if vtype == "float":
        return iiFloat(the_float=value)

    if vtype == "bool":
        if value == True:
            value = "true"
        else:
            value = "false"
        return iiBoolean(the_boolean=value)

    todo("CONVERSION: Cannot handle other value literals %s" % repr(arg))
    todo("CONVERSION: %s %s %s %d" % (tag, repr(value), repr(vtype), line))
    raise CannotConvert("Cannot convert value-literal of type" + repr(arg))



def convert_bool_operator_function(opfunc):
    DebugPrint("CONVERT - convert_bool_operator_function", repr(opfunc))
    assert isinstance(opfunc, nodes.PyBoolOperator)

    func = opfunc.tag
    arg1 = opfunc.argv[0]

    if not isinstance(opfunc, nodes.PyNotOperator):
        arg2 = opfunc.argv[1]
    else:
        arg2 = None

    crepr_arg1 = convert_arg(arg1)
    if arg2:
        crepr_arg2 = convert_arg(arg2)
    else:
        crepr_arg2 = None

    DebugPrint("crepr_arg1", repr(crepr_arg1))

    result = crepr_op(opfunc)

    DebugPrint(repr(result))
    return result


def convert_operator_function(opfunc):
    DebugPrint("CONVERT - convert_operator_function", repr(opfunc))
    assert isinstance(opfunc, nodes.PyOperator)

    func = opfunc.tag
    arg1 = opfunc.arg1
    arg2 = opfunc.arg2

    crepr_arg1 = convert_arg(arg1)
    crepr_arg2 = convert_arg(arg2)
    DebugPrint("crepr_arg1", repr(crepr_arg1))
    DebugPrint("crepr_arg2", repr(crepr_arg2))

    result = crepr_op(opfunc)
    DebugPrint(repr(result))
    return result

    #todo("Cannot yet convert operator functions")
    #raise CannotConvert("Cannot convert operator function :" + repr(arg))


def convert_comparison_operator(comparison):
    # t_NORMAL_COMPARISON_OPERATOR = r'(in|not +in|is|is +not)'

    if comparison in ["<", ">", "==", ">=", "<=", "<>", "!="]:
        return comparison

    raise NotImplementedError(repr(comparison))


def convert_comparison(comparison_spec):
    DebugPrint("CONVERT - convert_comparison", repr(comparison_spec))
    assert isinstance(comparison_spec, nodes.PyComparisonOperator)

    comparison = comparison_spec.comparison
    arg1 = comparison_spec.arg1
    arg2 = comparison_spec.arg2

    crepr_comparison = convert_comparison_operator(comparison)
    crepr_arg1 = convert_arg(arg1)
    crepr_arg2 = convert_arg(arg2)
    DebugPrint("crepr_arg1", repr(crepr_arg1))
    DebugPrint("crepr_arg2", repr(crepr_arg2))

    result = iiComparison(comparator=crepr_comparison, left=crepr_arg1, right=crepr_arg2)

    DebugPrint(repr(result))
    return result


def convert_arg(arg):
    if isinstance(arg, nodes.PyValueLiteral):
        DebugPrint("CONVERTING LITERAL", arg)
        return convert_value_literal(arg)
    elif isinstance(arg, nodes.PyComparisonOperator):
        return convert_comparison(arg)
    elif isinstance(arg, nodes.PyOperator):
        return convert_operator_function(arg)
    elif isinstance(arg, nodes.PyBoolOperator):
        return  convert_bool_operator_function(arg)

    elif isinstance(arg, nodes.PyFunctionCall):
        DebugPrint("NEED TO CONVERT FUNCTION CALL TO SOMETHING THE C CODE GENERATOR CAN HANDLE")
        cargs = []
        if arg.expr_list:
            for expr in arg.expr_list:
                #DebugPrint(arg)
                #DebugPrint("We need to convert the arg", arg)
                crepr = convert_arg(expr)
                carg = crepr
                cargs.append(carg)

        func_label = convert_value_literal(arg.func_label) # FIXME: func_label may not be an identifier...
        return iiFunctionCall(func_object=func_label, args=cargs)

    else:
        todo("Handle DebugPrint for non-value-literals")
        raise CannotConvert("Cannot convert DebugPrint for non-value-literals", arg)


def convert_print(print_statement):
    iistatement = []
    cargs = []
    for arg in print_statement.expr_list:
        #DebugPrint(arg)
        #DebugPrint("We need to convert the arg", arg)
        crepr = convert_arg(arg)
        carg = crepr
        cargs.append(carg)
    return mkPrintStatement(args=cargs)


def convert_while_statement(while_statement):
    crepr_condition = convert_arg(while_statement.condition)
    iistatements = convert_statements(while_statement.block)

    return iiWhileStatement(condition=crepr_condition, statements=iistatements)


def convert_for_statement(for_statement):

    lvalue = for_statement.identifier
    rvalue_source = for_statement.expression
    step = for_statement.block

    clvalue = lvalue.value # FIXME: This is only valid for identifiers


    crvalue_source = convert_arg(rvalue_source)
    crvalue_source = iiIterator(expression=crvalue_source)

    cstep = convert_statements(step)

    DebugPrint("*******************")
    DebugPrint(crvalue_source)
    DebugPrint("*******************")
    DebugPrint("FOR STATEMENT :")
    DebugPrint("              : ", for_statement)
    DebugPrint("              :", dir(for_statement))
    DebugPrint("     loop var :", for_statement.identifier)
    DebugPrint("loop var type :", for_statement.identifier.get_type())
    DebugPrint("loop var ctype:", python_type_to_c_type(for_statement.identifier.get_type()))
    DebugPrint("     iterator :", for_statement.expression)
    DebugPrint("        block :", for_statement.block)
    DebugPrint("        info :", for_statement.__info__())
    DebugPrint("*******************")
    DebugPrint( pprint.pformat(for_statement.__info__()) )
    DebugPrint("*******************")

    return iiForStatement(lvalue=clvalue, iterator=crvalue_source,
                          statements=cstep, for_statement_PyNode=for_statement)


def convert_def_statement(def_statement):
    DebugPrint("******************************************")
    DebugPrint("* CONVERT DEF STATEMENT ******************")
    DebugPrint("")
    DebugPrint("     :",def_statement)
    DebugPrint("NAME:", def_statement.identifier.value)
    DebugPrint("PARAMETERS:", def_statement.parameterlist)
    DebugPrint("BLOCK:", def_statement.block)
    DebugPrint("*******************")

    lvalue = def_statement.identifier
    cidentifer = lvalue.value # FIXME: This is only valid for identifiers

    cparamlist = None # TODO: This needs extending to parameters. This could be tricky...

    block = def_statement.block
    cblock = convert_statements(block)
    return iiDefStatement(name=cidentifer, params=cparamlist, block=cblock, def_statement_PyNode=def_statement)


def convert_extended_clause(extended_clause):
    if extended_clause.tag == "elif_clause":
        DebugPrint("WORKING THROUGH ELIF:", extended_clause)
        crepr_condition = convert_arg(extended_clause.condition)
        iistatements = convert_statements(extended_clause.block)
        if extended_clause.else_clause:
            cextended_clause = convert_extended_clause(extended_clause.else_clause)

            return iiElifClause(condition=crepr_condition, statements=iistatements,
                                extended_clause=cextended_clause)

        return iiElifClause(condition=crepr_condition, statements=iistatements)

    if extended_clause.tag == "else_clause":
        DebugPrint("WORKING THROUGH ELSE:", extended_clause)
        iistatements = convert_statements(extended_clause.block)

        return iiElseClause(statements=iistatements)

    DebugPrint("NOT ELIF!")
    DebugPrint("NOT ELSE!")
    DebugPrint(extended_clause)
    raise ValueError("Extended clause isn't a else or elif clause: %s" % repr(extended_clause))


def convert_if_statement(if_statement):
    DebugPrint("WORKING THROUGH IF:", if_statement)
    crepr_condition = convert_arg(if_statement.condition)
    iistatements = convert_statements(if_statement.block)
    if if_statement.else_clause:
        cextended_clause = convert_extended_clause(if_statement.else_clause)

        return iiIfStatement(condition=crepr_condition, statements=iistatements, extended_clause=cextended_clause)

    return iiIfStatement(condition=crepr_condition, statements=iistatements)


def convert_pass_statement(pass_statement):
    return iiPassStatement()


def convert_break_statement(break_statement):
    return iiBreakStatement()


def convert_continue_statement(continue_statement):
    return iiContinueStatement()


def convert_expression_statement(statement):
    DebugPrint("CONVERTING EXPRESSION STATEMENTS", statement.value)
    DebugPrint("EXPRESSION STATEMENT", statement.value.tag)
    crepr = convert_arg(statement.value)
    DebugPrint("REACHED HERE")
    DebugPrint("CONVERTED ", crepr)

    return iiExpressionStatement(expression=crepr)


def convert_statements(AST):
    iistatements = []
    statements = AST.statements
    for statement in statements:
        try:
            if statement.tag == "assignment_statement":
                iistatement = convert_assignment(statement)
                DebugPrint(iistatement)
                iistatements.append(iistatement)
            elif statement.tag == "print_statement":
                iistatement = convert_print(statement)
                iistatements.append(iistatement)
            elif statement.tag == "expression_statement":
                iistatement = convert_expression_statement(statement)
                iistatements.append(iistatement)
            elif statement.tag == "while_statement":
                iistatement = convert_while_statement(statement)
                iistatements.append(iistatement)
            elif statement.tag == "for_statement":
                iistatement = convert_for_statement(statement)
                iistatements.append(iistatement)
            elif statement.tag == "def_statement":
                iistatement = convert_def_statement(statement)
                iistatements.append(iistatement)
            elif statement.tag == "if_statement":
                iistatement = convert_if_statement(statement)
                iistatements.append(iistatement)
            elif statement.tag == "pass_statement":
                iistatement = convert_pass_statement(statement)
                iistatements.append(iistatement)
            elif statement.tag == "break_statement":
                iistatement = convert_break_statement(statement)
                iistatements.append(iistatement)
            elif statement.tag == "continue_statement":
                iistatement = convert_continue_statement(statement)
                iistatements.append(iistatement)
            else:
                print("SKIPPING STATEMENT", statement.tag)
                raise CannotConvert("Statement: "+ statement.tag)

        except CannotConvert:
            DebugPrint("REACHED HERE FOR", statement)
            raise

    return iistatements


def pynodes_to_iinodes(program_name, AST):
    cst = {}

    ast_includes = [x.replace("#include ","") for x in AST.includes]
    DebugPrint("AST.includes = ", ast_includes)

    # Extract and handle variables

    pvariables = find_variables(AST)
    cvariables = []
    ctypes = {}

    # includes = []
    includes = [x.replace("#include ","") for x in AST.includes]
    names = pvariables.keys()
    names.sort()
    for name in names:
        ctype = python_type_to_c_type(pvariables[name])

        identifier_declaration = iiIdentifierDeclaration(name=name, value_type=ctype)

        cvariables.append(identifier_declaration)
        ctypes[ctype] = True

    DebugPrint("cvariables",cvariables)

    iistatements = convert_statements(AST)
    DebugPrint(iistatements)

    # Based on variables, update includes
    for ctype in ctypes:
        inc = includes_for_ctype(ctype)
        if inc:
            includes.append(inc)

    DebugPrint("INCLUDES::", includes)
    # Based on statements, update includes
    for iistatement in iistatements:
        DebugPrint( "GETTING INCLUDES",  iistatement  )
        inc = includes_for_iistatement(iistatement)
        if inc:
            includes.append(inc)

    program = iiProgram(name=program_name, includes=includes, identifiers=cvariables, statements=iistatements)
    return program



if __name__ == "__main__":
    pass