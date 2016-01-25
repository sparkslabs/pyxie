#!/usr/bin/python
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

import sys
import json

# These imports are pretty icky, but appropriate in this context

from .util import *
from .base_nodes import *
from .statements import *
from .operators import *

from pyxie.parsing.context import Context

MULTI_TYPES_WARN = False
WARNINGS_ARE_FAILURES = False

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
        print("ANALYSING PROGRAM")

        global_context = Context()
        for node in self.depth_walk():
            if node.tag == "identifier":
                node.context = global_context
                print("NODE", node)

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
        print("ANALYSING BLOCK")

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
        print("ANALYSING STATEMENTS")
        self.ntype = self.get_type()
        for statement in self.statements:
            statement.analyse() # Descend through the tree

    def get_type(self):
        # Block of statements has no value, so no type
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

class PyAttribute(PyNode):
    tag = "attribute"
    def __init__(self, lineno, value):
        super(PyAttribute, self).__init__()
        self.lineno = lineno
        self.value = value

    def __repr__(self):
        return "%s(%d, %s)" % (self.classname(),self.lineno, repr(self.value))

    def __json__(self):
        return [ self.tag, self.lineno, jdump(self.value) ]

class PyAttributeAccess(PyNode):
    tag = "attributeaccess"
    def __init__(self, expression, attribute):
        super(PyAttributeAccess,self).__init__()
        self.expression = expression
        self.attribute = attribute

    def __repr__(self):
        return "%s(%s, %s)" % (self.classname(), repr(self.expression), repr(self.attribute))

    def __json__(self):
        return [ self.tag, jdump(self.expression), jdump(self.attribute) ]

#    def value(self):
#        return self.attribute

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
        print("ANALYSING VALUE LITERAL", self.tag)
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

class PySignedLong(PyNumber):
    tag = "signedlong"
    def get_type(self):
        return "signedlong"

class PyUnSignedLong(PyNumber):
    tag = "unsignedlong"
    def get_type(self):
        return "unsignedlong"

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
        print(tree)

    for tree in trees:
        print(jdump(tree))

    MULTI_TYPES_WARN = True
    WARNINGS_ARE_FAILURES = False

    ident = PyIdentifier(1,"hello")
    print(ident, ident.get_type())

    ident.add_type("string")
    print(ident, ident.get_type())
    ident.add_type("string")
    print(ident, ident.get_type())
    ident.add_type("char")
    print(ident, ident.get_type())
    ident.add_type("integer")
    print(ident, ident.get_type())
    ident.add_type("float")
    print(ident, ident.get_type())
    ident.add_type("bool")
    print(ident, ident.get_type())

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
        print(tree, tree.get_type())
