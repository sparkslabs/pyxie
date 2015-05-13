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

import json

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

def jdump(thing):
    "Calls __json__ on a thing to try and convert it into a json serialisable thing"
    try:
        return thing.__json__()
    except AttributeError:
        print "WARNING", thing, "is not a pynode"


class PyNode(object):
    """Representation of a python node"""
    def __init__(self, *args):
        raise Exception("Abstract Class")
    def tags(self):
        return ["node"]
    def classname(self):
        return self.__class__.__name__

class PyOperation(PyNode):
    tag = "operation"
    def __init__(self, *args):
        raise Exception("Abstract Class")



class PyStatement(PyNode):
    tag = "statement"
    def __init__(self, *args):
        raise Exception("Abstract Class")

class PyAssignment(PyStatement):
    tag = "assignment_statement"
    def __init__(self, lvalue, rvalue, assign_type):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.assign_type = assign_type
    def __repr__(self):
        return "PyAssignment(%s,%s,%s)" % (repr(self.lvalue), repr(self.rvalue), repr(self.assign_type))
    def __json__(self):
        return [ self.tag, jdump(self.lvalue), jdump(self.rvalue), self.assign_type ]



class PyExpressionStatement(PyStatement):
    tag = "expression_statement"
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return "PyExpressionStatement(%s)" % (repr(self.value), )
    def __json__(self):
        return [ self.tag, jdump(self.value) ]

class PyPrintStatement(PyStatement):
    tag = "print_statement"
    def __init__(self, expr_list):
        self.expr_list = expr_list
    def __repr__(self):
        return "PyPrintStatement(%s)" % (repr(self.expr_list), )
    def __json__(self):
        return [ self.tag, jdump(self.expr_list) ]

class PyProgram(PyNode):
    tag = "program"
    def __init__(self, statements):
        self.statements = statements
    def __repr__(self):
        return "PyProgram(%s)" % (repr(self.statements), )
    def __json__(self):
        return [ self.tag, jdump(self.statements) ]


class PyStatements(PyNode):
    tag = "statements"
    def __init__(self, head, *tail):
        self.statements = [ head ]
        if tail:
            for node in tail:
                self.statements = self.statements + node.statements

    def __repr__(self):
        return "PyStatements(%s)" % ",\n ".join([repr(x) for x in self.statements])

    def __json__(self):
        return [self.tag, [ jdump(x) for x in self.statements] ]

    def __iter__(self):
        for statement in self.statements:
            yield statement

class PyExprList(PyNode):
    tag = "expression_list"
    def __init__(self, expr, *tail):
        self.expressions = [ expr ]
        if tail:
            for node in tail:
                self.expressions = self.expressions + node.expressions

    def __repr__(self):
        return "PyExprList(%s)" % ",\n ".join([repr(x) for x in self.expressions])

    def __json__(self):
        return [self.tag, [ jdump(x) for x in self.expressions] ]

    def __iter__(self):
        for expression in self.expressions:
            yield expression


class PyOperator(PyOperation):
    tag = "operator"
    def __init__(self, arg1, arg2):
        self.arg1 = arg1
        self.arg2 = arg2
        self._type = None

    @property
    def type(self):
        if self._type != None:
            return self._type
        try:
            if self.arg1.get_type() == self.arg2.get_type():
                self._type = self.arg1.get_type()
            elif (self.tag, self.arg1.get_type(),self.arg2.get_type()) in expression_mixed_types:
                self._type = expression_mixed_types[self.tag, self.arg1.get_type(),self.arg2.get_type()]
            else:
                self._type = "Mixed types, need to resolve", self.tag, self.arg1.get_type(),self.arg2.get_type()
            return self._type
        except:
            print "TAG", self.tag
            print "ARG1", self.arg1.get_type()
            print "ARG2", self.arg2.get_type()
            raise

    def __repr__(self):
        return "%s(%s, %s)" % (self.classname(),repr(self.arg1),repr(self.arg1))
    def __json__(self):
        return [ self.tag, jdump(self.arg1), jdump(self.arg2) ]
    def get_type(self):
        return self.type

class PyValueLiteral(PyNode):
    tag = "value_literal"
    def __init__(self, lineno, value):
        self.lineno = lineno
        self.value = value
    def __repr__(self):
        return "%s(%d, %s)" % (self.classname(),self.lineno, repr(self.value))
    def __json__(self):
        return [ self.tag, self.lineno, self.value ]

class PyTimesOperator(PyOperator):
    tag = "op_times"

class PyDivideOperator(PyOperator):
    tag = "op_divide"

class PyPowerOperator(PyOperator):
    tag = "op_power"

class PyPlusOperator(PyOperator):
    tag = "op_plus"

class PyMinusOperator(PyOperator):
    tag = "op_minus"

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

def warn(message):
    if WARNINGS_ARE_FAILURES:
        raise Exception(message)
    else:
        print message

# Resist the urge to put PyIdentifiers into a LUT immediately.
class PyIdentifier(PyValueLiteral):
    tag = "identifier"
    def __init__(self, context, *args):
        super(PyIdentifier, self).__init__(*args)
        self.context = context
        self.types = []

    def add_type(self, pytype):
        if pytype not in self.types:
            self.types.append(pytype)
        if len(self.types)>1:
            if MULTI_TYPES_WARN:
                err = "Warning: Identifier %s at line %d can have conflicting types %s" %(self.value, self.lineno, repr(self.types))
                warn(err)

    def get_type(self):
        try:
            v_type = self.context.lookup(self.value)
            return v_type
        except: # FIXME: Contextleakage exception - badly named...
            print "We failed and reached here >>" + str( self.value) +"<<"
            pass

        if len(self.types) == 0:
            err = "GT Warning: Identifier %s at line %d has no identified type" %(self.value, self.lineno )
            warn(err)
        if self.context:
            print "self.context", self.context.lookup(self.value)
        if len(self.types) > 0:
            self.context.store(self.value, self.types[0])
            return self.types[0]
        else:
            return None

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


