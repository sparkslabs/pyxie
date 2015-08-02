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

import sys
import json

from pyxie.parsing.context import Context
from pyxie.model.tree import Tree
from pyxie.model.functions import builtins

MULTI_TYPES_WARN = False
WARNINGS_ARE_FAILURES = False

# This lookup should probably really look somewhere else
expression_mixed_types = {
       #(function_tag, type, type ) -> result_type
        ("op_times", "integer", "string") : "string",
        ("op_times", "string","integer") : "string",
        ("op_times", "integer", "char") : "string",
        ("op_times", "char","integer") : "string",
    }

# Utility functions

def jdump(thing):
    "Calls __json__ on a thing to try and convert it into a json serialisable thing"
    try:
        return thing.__json__()
    except AttributeError:
        print "WARNING::", repr(thing), "is not a pynode"
        print "       ::", type(thing)

def warn(message):
    if WARNINGS_ARE_FAILURES:
        raise Exception(message)
    else:
        print message

# Astract base nodes

class PyNode(Tree):
    """Representation of a python node"""
    tag = "node"
    ntype = None # Type for this node
    def __init__(self, *args):
        # Initialise the tree
        super(PyNode,self).__init__()
    def tags(self):
        return ["node"]
    def classname(self):
        return self.__class__.__name__
    def __info__(self):
        return { self.tag : {"type":self.ntype} }

class PyOperation(PyNode):
    tag = "operation"
    def __init__(self, *args):
        super(PyOperation,self).__init__()

class PyStatement(PyNode):
    tag = "statement"
    def __init__(self, *args):
        super(PyStatement,self).__init__()

# Grammar nodes, in approximate grammar order

class PyProgram(PyNode):
    tag = "program"
    def __init__(self, statements):
        super(PyProgram,self).__init__()
        self.statements = statements
        self.includes = None
        self.add_children(statements)
    def __repr__(self):
        return "PyProgram(%s)" % (repr(self.statements), )
    def __json__(self):
        return [ self.tag, jdump(self.statements) ]

    def __info__(self):
        info = super(PyProgram, self).__info__()
        info[self.tag].update(self.statements.__info__())
        contexts = Context.contexts
        contexts_info = []
        for context in contexts:
            contexts_info.append(contexts[context].__json__())
        info[self.tag]["contexts"] = contexts_info
        return info

    def analyse(self):
        print "ANALYSING PROGRAM"

        global_context = Context()
        for node in self.depth_walk():
            if node.tag == "identifier":
                node.context = global_context
                print "NODE", node

        self.ntype = self.get_type()
        self.statements.analyse() # Descend through the tree

    def get_type(self):
        # Program has no value so no type
        return None

class PyBlock(PyNode):
    tag = "block"
    def __init__(self, statements):
        super(PyBlock,self).__init__()
        self.statements = statements
        self.add_children(statements)
    def __repr__(self):
        return "PyBlock(%s)" % (repr(self.statements), )
    def __json__(self):
        return [ self.tag, jdump(self.statements) ]

    def __info__(self):
        # Minimal change from "Program, since might be considered similar)
        # That said, I suspect that's wrong since a BLOCK doesn't necessarily
        # have a new context. Commenting that out for the moment.
        info = super(PyBlock, self).__info__()
        info[self.tag].update(self.statements.__info__())
#        contexts = Context.contexts
#        contexts_info = []
#        for context in contexts:
#            contexts_info.append(contexts[context].__json__())
#        info[self.tag]["contexts"] = contexts_info
        return info

    def analyse(self):
        print "ANALYSING BLOCK"

#        global_context = Context()
#        for node in self.depth_walk():
#            if node.tag == "identifier":
#                node.context = global_context

        self.ntype = None
        self.statements.analyse() # Descend through the tree

    def get_type(self):
        # Program has no value so no type
        return None

class PyStatements(PyNode):
    tag = "statements"
    def __init__(self, head, *tail):
        super(PyStatements,self).__init__()
        if not isinstance(head, PyEmptyStatement): #Filter out empty statements here.
            self.statements = [ head ]
        else:
            self.statements = [ ]
        if tail:
            for node in tail:
                self.statements = self.statements + node.statements
        if len(self.statements) > 0:
            self.add_children(*(self.statements))

    def __info__(self):
        info = super(PyStatements, self).__info__()
        info[self.tag]["block"] = [ x.__info__() for x in self.statements]
        return info

    def __repr__(self):
        return "PyStatements(%s)" % ",\n ".join([repr(x) for x in self.statements])

    def __json__(self):
        return [self.tag, [ jdump(x) for x in self.statements] ]

    def __iter__(self):
        for statement in self.statements:
            yield statement

    def analyse(self):
        print "ANALYSING STATEMENTS"
        self.ntype = self.get_type()
        for statement in self.statements:
            statement.analyse() # Descend through the tree

    def get_type(self):
        # Block of statements has no value, so no type
        return None

class PyAssignment(PyStatement):
    tag = "assignment_statement"
    def __init__(self, lvalue, rvalue, assign_type):
        super(PyAssignment,self).__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.assign_type = assign_type
        self.add_children(self.lvalue, self.rvalue)

    def __repr__(self):
        return "PyAssignment(%s,%s,%s)" % (repr(self.lvalue), repr(self.rvalue), repr(self.assign_type))
    def __json__(self):
        return [ self.tag, jdump(self.lvalue), jdump(self.rvalue), self.assign_type ]

    def __info__(self):
        info = super(PyAssignment, self).__info__()
        info[self.tag]["lvalue"] = self.lvalue.__info__()
        info[self.tag]["rvalue"] = self.rvalue.__info__()
        info[self.tag]["assign_type"] = self.assign_type
        return info

    def analyse(self):
        print "ANALYSING ASSIGNMENT"
        print "ANALYSE RIGHT"
        self.rvalue.analyse()
        self.lvalue.add_rvalue(self.rvalue)
        self.lvalue.analyse()

        self.ntype = self.get_type()

    def get_type(self):
        ltype = self.lvalue.get_type()
        rtype = self.rvalue.get_type()

        print "Type for lvalue:", ltype
        print "Type for rvalue:", rtype
        print "Types match:", rtype==ltype

        # rtype wins because it's being used to set the left
        return rtype

class PyExpressionStatement(PyStatement):
    tag = "expression_statement"
    def __init__(self, value):
        super(PyExpressionStatement,self).__init__()
        self.value = value
        self.add_children(value)

    def __repr__(self):
        return "PyExpressionStatement(%s)" % (repr(self.value), )
    def __json__(self):
        return [ self.tag, jdump(self.value) ]
    def __info__(self):
        info = super(PyExpressionStatement, self).__info__()
        info[self.tag]["value"] = self.value.__info__()
        return info
    def analyse(self):
        print "ANALYSING EXPRESSION STATEMENT"
        self.value.analyse()
        self.ntype = self.get_type()
    def get_type(self):
        return self.value.get_type()

class PyFunctionCall(PyStatement):
    tag = "function_call"
    def __init__(self, identifier, expr_list):
        super(PyFunctionCall,self).__init__()
        self.identifier = identifier
        self.expr_list = expr_list
        if expr_list:
            self.add_children(expr_list)
        self.builtin = False
        self.isiterator = False
    def __repr__(self):
        if self.expr_list:
            return "PyFunctionCall(%s, %s)" % (repr(self.identifier), repr(self.expr_list), )
        else:
            return "PyFunctionCall(%s)" % (repr(self.identifier), )

    def __json__(self):
        if self.expr_list:
            return [ self.tag, jdump(self.identifier), jdump(self.expr_list) ]
        else:
            return [ self.tag, jdump(self.identifier) ]
    def __info__(self):
        info = super(PyFunctionCall, self).__info__()
        info[self.tag]["name"] = self.identifier.__info__()
        if self.expr_list:
            info[self.tag]["args"] = [ x.__info__() for x in self.expr_list ]
        else:
            info[self.tag]["args"] = []
        return info

    def analyse(self):
        # We'll need to decorate the function call with information from somewhere
        # For now though, we won't
        print "ANALYSING FUNCTION CALL"
        if self.identifier.value in builtins:
            print "FUNCTION", self.identifier.value, "FOUND IN BUILTINS"
            self.builtin = True
            self.ntype = self.get_type()
            print "WE CAN DO ANALYSIS FOR LIMITED BUILTINS"
            print " IS AN ITERATOR:", self.isiterator
            print "  VALUE(S) TYPE:", self.ntype
            return
        print "NOTE: WE DON'T ACTUALLY DO ANY ANALYSIS YET - GENERALLY"
        print "NOTE: ASIDE FROM SPECIAL CASING WE'LL JUST PASS THROUGH"
        return

    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        if self.builtin:
            print "It's a built in function, we can get it's type in a bit..."
            meta = builtins[self.identifier.value]
            self.isiterator = meta.get("iterator", False)
            if self.isiterator:
                return meta.get("values_type", None)
            return meta.get("return_type", None)
        print "GETTING FUNCTION TYPE"
        print "NOTE: WE CAN'T ACTUALLY GET THE TYPE YET"
        print "NOTE: ASIDE FROM SPECIAL CASING WE'LL JUST CROSS FINGERS FOR NOW"
        return None

class PyForLoop(PyStatement):
    tag = "for_statement"
    def __init__(self, identifier, expression, block):
        super(PyForLoop,self).__init__()
        self.identifier= identifier
        self.expression = expression
        self.block = block
        self.add_children(identifier, expression, block)
    def __repr__(self):
        return "PyForLoop(%s, %s, %s)" % (repr(self.identifier), repr(self.expression), repr(self.block) )
    def __json__(self):
        return [ self.tag, jdump(self.identifier), jdump(self.expression), jdump(self.block) ]
    def __info__(self):
        info = super(PyForLoop, self).__info__()
        info[self.tag]["identifier"] = self.identifier.__info__()
        info[self.tag]["block"] = self.block.__info__()
        info[self.tag]["expression"] = self.expression.__info__()
        return info
    def analyse(self):
        # We'll need to decorate the function call with information from somewhere
        # For now though, we won't
        print "ANALYSING FOOR LOOP"
        print"                ... Analyse expression"
        expression = self.expression
        expression.analyse()
        print expression
        if expression.isiterator:
            print "Expression is an iterator"

        self.identifier.add_rvalue(expression) # The result of the expression becomes a repeated rvalue for the identifier, so this sorta makes sense

        print"                ... Update identifier"
        print"                ... Analyse identifier"
        self.identifier.analyse()

        print"                ... Analyse block"
        self.block.analyse()
        return

class PyWhileStatement(PyStatement):
    tag = "while_statement"
    def __init__(self, condition, block):
        super(PyWhileStatement,self).__init__()
        self.condition = condition
        self.block = block
        self.add_children(condition, block)
    def __repr__(self):
        return "PyWhileStatement(%s, %s)" % (repr(self.condition), repr(self.block) )
    def __json__(self):
        return [ self.tag, jdump(self.condition), jdump(self.block) ]
    def __info__(self):
        info = super(PyWhileStatement, self).__info__()
        info[self.tag]["condition"] = self.condition.__info__()
        # info[self.tag]["block"] = [ x.__info__() for x in self.expr_list ]
        info[self.tag]["block"] = self.block.__info__()
        return info
    def analyse(self):
        # We'll need to decorate the function call with information from somewhere
        # For now though, we won't
        print "ANALYSING WHILE BLOCK"
        print "analyse expression, and analyse block"
        self.condition.analyse()
        self.block.analyse()
        return
    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        print "GETTING WHILE BLOCK TYPE - which should be None - for now"
        return None

class PyIfStatement(PyStatement):
    tag = "if_statement"
    def __init__(self, condition, block, else_clause=None):
        super(PyIfStatement,self).__init__()
        self.condition = condition
        self.block = block
        self.else_clause = else_clause
        self.add_children(condition, block)
    def __repr__(self):
        else_clause = ""
        if self.else_clause:
            else_clause = ", %s" % (repr(self.else_clause),)
        return "PyIfStatement(%s, %s%s)" % (repr(self.condition), repr(self.block), else_clause)
    def __json__(self):
        else_clause = ""
        if self.else_clause:
            else_clause = jdump(self.else_clause)
        return [ self.tag, jdump(self.condition), jdump(self.block), "", else_clause ] # Space left for elif chain...

    def __info__(self):
        info = super(PyIfStatement, self).__info__()
        info[self.tag]["condition"] = self.condition.__info__()
        info[self.tag]["block"] = self.block.__info__()
        if self.else_clause:
            info[self.tag]["else_clause"] = self.else_clause.__info__()
        return info
    def analyse(self):
        print "ANALYSING IF BLOCK"
        print "analyse expression, and analyse block"
        self.condition.analyse()
        self.block.analyse()
        if self.else_clause:
            self.else_clause.analyse()
        return
    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        print "GETTING IF BLOCK TYPE - which should be None - for now"
        return None

class PyElIfClause(PyStatement):
    tag = "elif_clause"
    def __init__(self, condition, block, else_clause=None):
        super(PyElIfClause,self).__init__()
        self.condition = condition
        self.block = block
        self.else_clause = else_clause
        self.add_children(condition, block)
    def __repr__(self):
        else_clause = ""
        if self.else_clause:
            else_clause = ", %s" % (repr(self.else_clause),)
        return "PyElIfClause(%s, %s%s)" % (repr(self.condition), repr(self.block), else_clause)
    def __json__(self):
        else_clause = ""
        if self.else_clause:
            else_clause = jdump(self.else_clause)
        return [ self.tag, jdump(self.condition), jdump(self.block), "", else_clause ] # Space left for elif chain...

    def __info__(self):
        info = super(PyElIfClause, self).__info__()
        info[self.tag]["condition"] = self.condition.__info__()
        info[self.tag]["block"] = self.block.__info__()
        if self.else_clause:
            info[self.tag]["else_clause"] = self.else_clause.__info__()
        return info
    def analyse(self):
        print "ANALYSING ELIF BLOCK"
        print "analyse expression, and analyse block"
        self.condition.analyse()
        self.block.analyse()
        if self.else_clause:
            self.else_clause.analyse()
        return
    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        print "GETTING IF BLOCK TYPE - which should be None - for now"
        return None

class PyElseClause(PyStatement):
    tag = "else_clause"
    def __init__(self, block):
        super(PyElseClause,self).__init__()
        self.block = block
        self.add_children(block)
    def __repr__(self):
        return "PyElseClause(%s)" % (repr(self.block), )
    def __json__(self):
        return [ self.tag, jdump(self.block) ]
    def __info__(self):
        info = super(PyElseClause, self).__info__()
        info[self.tag]["block"] = self.block.__info__()
        return info
    def analyse(self):
        print "ANALYSING ELSE CLAUSE"
        print "analyse expression, and analyse block"
        self.block.analyse()
        return
    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        print "GETTING ELSE CLAUSE TYPE - which should be None - for now"
        return None

class PyEmptyStatement(PyStatement):
    tag = "empty_statement"
    def __init__(self):
        super(PyEmptyStatement,self).__init__()
    def analyse(self):
        pass
    def __json__(self):
        return [ self.tag ]

class PyBreakStatement(PyStatement):
    tag = "break_statement"
    def __init__(self):
        super(PyBreakStatement,self).__init__()
    def analyse(self):
        pass
    def __json__(self):
        return [ self.tag ]

class PyContinueStatement(PyStatement):
    tag = "continue_statement"
    def __init__(self):
        super(PyContinueStatement,self).__init__()
    def analyse(self):
        pass
    def __json__(self):
        return [ self.tag ]

class PyPrintStatement(PyStatement):
    tag = "print_statement"
    def __init__(self, expr_list):
        super(PyPrintStatement,self).__init__()
        self.expr_list = expr_list
        self.add_children(expr_list)

    def __repr__(self):
        return "PyPrintStatement(%s)" % (repr(self.expr_list), )
    def __json__(self):
        return [ self.tag, jdump(self.expr_list) ]
    def __info__(self):
        info = super(PyPrintStatement, self).__info__()
        info[self.tag]["args"] = [ x.__info__() for x in self.expr_list ]
        return info
    def analyse(self):
        print "ANALYSING PRINT STATEMENT"
        for expr in self.expr_list:
            expr.analyse() # Descend through the tree

        self.ntype = self.get_type()
    def get_type(self):
        # Print statement has no return value or default value
        return None

class PyExprList(PyNode):
    tag = "expression_list"
    def __init__(self, expr, *tail):
        super(PyExprList,self).__init__()
        self.expressions = [ expr ]
        if tail:
            for node in tail:
                self.expressions = self.expressions + node.expressions
        self.add_children(*(self.expressions))

    def __repr__(self):
        return "PyExprList(%s)" % ",\n ".join([repr(x) for x in self.expressions])

    def __json__(self):
        return [self.tag, [ jdump(x) for x in self.expressions] ]

    def __iter__(self):
        for expression in self.expressions:
            yield expression

    def __info__(self):
        raise Exception("Expression List should not have info called directly")

    def analyse(self):
        raise Exception("Expression List should not have analyse called directly")

# Base node for expressions, and all operators
class PyOperator(PyOperation):
    tag = "operator"
    def __init__(self, arg1, arg2):
        super(PyOperator,self).__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.ntype = None
        self.add_children(arg1,arg2)

    def __info__(self):
        info = super(PyOperator, self).__info__()
        info[self.tag]["arg1"] = self.arg1.__info__()
        info[self.tag]["arg2"] = self.arg2.__info__()
        return info

    @property
    def type(self):
        if self.ntype != None:
            return self.ntype
        try:
            if self.arg1.get_type() == self.arg2.get_type():
                self.ntype = self.arg1.get_type()
            elif (self.tag, self.arg1.get_type(),self.arg2.get_type()) in expression_mixed_types:
                self.ntype = expression_mixed_types[self.tag, self.arg1.get_type(),self.arg2.get_type()]
            else:
                self.ntype = "Mixed types, need to resolve", self.tag, self.arg1.get_type(),self.arg2.get_type()
            return self.ntype
        except:
            print "TAG", self.tag
            print "ARG1", self.arg1.get_type()
            print "ARG2", self.arg2.get_type()
            raise

    def __repr__(self):
        return "%s(%s, %s)" % (self.classname(),repr(self.arg1),repr(self.arg2))
    def __json__(self):
        return [ self.tag, jdump(self.arg1), jdump(self.arg2) ]
    def get_type(self):
        return self.type
    def analyse(self):
        print "ANALYSING OPERATOR", self.tag
        self.arg1.analyse()
        self.arg2.analyse()

        self.ntype = self.get_type()

class PyBoolOperator(PyOperation):
    pass

class PyOrOperator(PyBoolOperator):
    tag = "or_operator"
    def __init__(self, arg1, arg2):
        super(PyOrOperator,self).__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.ntype = None
        self.add_children(arg1,arg2)

    def __info__(self):
        info = super(PyOrOperator, self).__info__()
        info[self.tag]["arg1"] = self.arg1.__info__()
        info[self.tag]["arg2"] = self.arg2.__info__()
        return info

    @property
    def type(self):
        return "bool"

    def __repr__(self):
        return "%s(%s, %s)" % (self.classname(),repr(self.arg1),repr(self.arg2))
    def __json__(self):
        return [ self.tag, jdump(self.arg1), jdump(self.arg2) ]
    def get_type(self):
        return "bool"
    def analyse(self):
        print "ANALYSING OPERATOR:", self.tag
        self.arg1.analyse()
        self.arg2.analyse()

        self.ntype = self.get_type()

class PyAndOperator(PyBoolOperator):
    tag = "and_operator"
    def __init__(self, arg1, arg2):
        super(PyAndOperator,self).__init__()
        self.arg1 = arg1
        self.arg2 = arg2
        self.ntype = None
        self.add_children(arg1,arg2)

    def __info__(self):
        info = super(PyAndOperator, self).__info__()
        info[self.tag]["arg1"] = self.arg1.__info__()
        info[self.tag]["arg2"] = self.arg2.__info__()
        return info

    @property
    def type(self):
        return "bool"

    def __repr__(self):
        return "%s(%s, %s)" % (self.classname(),repr(self.arg1),repr(self.arg2))
    def __json__(self):
        return [ self.tag, jdump(self.arg1), jdump(self.arg2) ]
    def get_type(self):
        return "bool"
    def analyse(self):
        print "ANALYSING OPERATOR:", self.tag
        self.arg1.analyse()
        self.arg2.analyse()

        self.ntype = self.get_type()

class PyNotOperator(PyBoolOperator):
    tag = "not_operator"
    def __init__(self, arg1):
        super(PyNotOperator,self).__init__()
        self.arg1 = arg1
        self.ntype = None
        self.add_children(arg1)

    def __info__(self):
        info = super(PyNotOperator, self).__info__()
        info[self.tag]["arg1"] = self.arg1.__info__()
        return info

    @property
    def type(self):
        return "bool"

    def __repr__(self):
        return "%s(%s)" % (self.classname(),repr(self.arg1),)
    def __json__(self):
        return [ self.tag, jdump(self.arg1) ]
    def get_type(self):
        return "bool"
    def analyse(self):
        print "ANALYSING OPERATOR:", self.tag
        self.arg1.analyse()
        self.ntype = self.get_type()

class PyTimesOperator(PyOperator):
    tag = "op_times"

class PyDivideOperator(PyOperator):
    tag = "op_divide"

class PyPowerOperator(PyOperator):
    tag = "op_power"

class PyPlusOperator(PyOperator):
    tag = "op_plus"

class PyComparisonOperator(PyOperation):
    tag = "comparison_operator"
    def __init__(self, comparison, arg1, arg2):
        super(PyComparisonOperator,self).__init__()
        self.comparison = comparison
        self.arg1 = arg1
        self.arg2 = arg2
        self.ntype = None
        self.add_children(arg1,arg2)

        print "CREATED COMPARISON OPERATOR", comparison, arg1, arg2

    def __info__(self):
        info = super(PyComparisonOperator, self).__info__()
        info[self.tag]["comparison"] = self.comparison
        info[self.tag]["arg1"] = self.arg1.__info__()
        info[self.tag]["arg2"] = self.arg2.__info__()
        return info

    @property
    def type(self):
        return "bool"

    def __repr__(self):
        return "%s(%s, %s, %s)" % (self.classname(),self.comparison, repr(self.arg1),repr(self.arg2))
    def __json__(self):
        return [ self.tag, self.comparison, jdump(self.arg1), jdump(self.arg2) ]
    def get_type(self):
        return "bool"
    def analyse(self):
        print "ANALYSING", self.tag
        self.arg1.analyse()
        self.arg2.analyse()

        self.ntype = self.get_type()

class PyMinusOperator(PyOperator):
    tag = "op_minus"

# Base class for all Value Literals
class PyValueLiteral(PyNode):
    tag = "value_literal"
    def __init__(self, lineno, value):
        super(PyValueLiteral,self).__init__()
        self.lineno = lineno
        self.value = value
    def __repr__(self):
        return "%s(%d, %s)" % (self.classname(),self.lineno, repr(self.value))
    def __json__(self):
        return [ self.tag, self.lineno, self.value ]
    def __info__(self):
        info = super(PyValueLiteral, self).__info__()
        info[self.tag]["lineno"] = self.lineno
        info[self.tag]["value"] = self.value
        return info
    def analyse(self):
        print "ANALYSING VALUE LITERAL", self.tag
        # Don't go into containers, because there aren't any
        self.ntype = self.get_type()
    def get_type(self):
        raise NotImplementedError("PyValueLiteral does not have any implicit type - its subtypes do")

# All non-number value literals first
class PyString(PyValueLiteral):
    tag = "string"
    def get_type(self):
        return "string"

class PyCharacter(PyValueLiteral):
    tag = "character"
    def get_type(self):
        return "char"

class PyBoolean(PyValueLiteral):
    tag = "boolean"
    def get_type(self):
        return "bool"

# Resist the urge to put PyIdentifiers into a LUT immediately.
class PyIdentifier(PyValueLiteral):
    tag = "identifier"
    def __init__(self, *args):
        super(PyIdentifier, self).__init__(*args)
        self.context = None
        self.types = []

    def add_rvalue(self, expression):
        self.context.store(self.value, expression)

    def __info__(self):
        info = super(PyIdentifier, self).__info__()
        info[self.tag]["context "] = self.context
        info[self.tag]["types"] = self.types
        return info

    def get_type(self):
        return self.ntype

    def analyse(self):
        expression = self.context.lookup(self.value)
        self.ntype = expression.get_type()

# Base class for all numbers
class PyNumber(PyValueLiteral):
    tag = "number"
    def negate(self):
        self.value = - self.value
        return self

class PyFloat(PyNumber):
    tag = "float"
    def get_type(self):
        return "float"

class PyInteger(PyNumber):
    tag = "integer"
    def get_type(self):
        return "integer"

class PyHex(PyNumber):
    tag = "hex"
    def get_type(self):
        return "integer"

class PyOctal(PyNumber):
    tag = "octal"
    def get_type(self):
        return "integer"

class PyBinary(PyNumber):
    tag = "binary"
    def get_type(self):
        return "integer"

if __name__ == "__main__":
    trees = [
                PyMinusOperator(PyInteger(1,10),PyInteger(1,10)),
                PyBoolean(1,True),
                PyAssignment(PyIdentifier(1,"hello"), PyString(1,"world"), "="),
                PyExpressionStatement(PyMinusOperator(PyInteger(1,10),PyInteger(1,10)))
        ]
    for tree in trees:
        print tree

    for tree in trees:
        print jdump(tree)

    MULTI_TYPES_WARN = True
    WARNINGS_ARE_FAILURES = False

    ident = PyIdentifier(1,"hello")
    print ident, ident.get_type()

    ident.add_type("string")
    print ident, ident.get_type()
    ident.add_type("string")
    print ident, ident.get_type()
    ident.add_type("char")
    print ident, ident.get_type()
    ident.add_type("integer")
    print ident, ident.get_type()
    ident.add_type("float")
    print ident, ident.get_type()
    ident.add_type("bool")
    print ident, ident.get_type()

    trees = [
                PyString(1,"world"),
                PyBoolean(1,True),
                PyFloat(1,1.1),
                PyMinusOperator(PyInteger(1,10),PyInteger(1,10)),
                PyMinusOperator(PyFloat(1,10),PyFloat(1,10)),
                PyTimesOperator(PyInteger(1,10),PyString(1,"Hello")),
                PyTimesOperator(PyString(1,"Hello"),PyInteger(1,10)),
                PyTimesOperator(PyInteger(1,10),PyCharacter(1,"Hello")),
                PyTimesOperator(PyCharacter(1,"Hello"),PyInteger(1,10)),
                PyTimesOperator(PyInteger(1,10),PyBoolean(1,True)),
                PyTimesOperator(PyCharacter(1,"Hello"),PyFloat(1,1.1)),
                PyPlusOperator(PyInteger(1,10),PyString(1,"Hello")),

            ]

    for tree in trees:
        print tree, tree.get_type()

    #print PyMinusOperator(PyInteger(1,10),PyInteger(1,10))
    #print jdump(PyMinusOperator(PyInteger(1,10),PyInteger(1,10)))

    #print PyBoolean(1,True)
    #print jdump(PyBoolean(1,True))

    #print PyAssignment(PyIdentifier(1,"hello"), PyString(1,"world"), "=")

    #print jdump(PyAssignment(PyIdentifier(1,"hello"), PyString(1,"world"), "="))


