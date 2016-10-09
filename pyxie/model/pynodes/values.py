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

from __future__ import print_function
from __future__ import absolute_import

import inspect

from .util import *
from .base_nodes import PyNode

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
        print("PyIdentifier.analyse", self.value, self, dir(self))
        for i in dir(self):
            if i.startswith("__") and i.endswith("__"):
                continue
            if "bound method" in repr(getattr(self, i)):
                continue
            print("attr", i, repr(getattr(self, i)), getattr(self, i) )
        expression = self.context.lookup(self.value)
        self.ntype = expression.get_type()

    # FIXME: This name is created to allow attribute access lookup
    def name(self):
        return self.value

class ProfilePyNode(PyIdentifier):
    """Representation of something in the python code that's external to it - from a profile"""
    tag = "profile_identifier"
    def __init__(self, name, value_type):
        self.lineno = 0
        self.value = name
        #super(ProfilePyNode,self).__init__()
        self.ntype = value_type # Logical type of this virtual valie
    def analyse(self):
        self.ntype = expression.get_type()
    def get_type(self):
        return self.ntype


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

    def name(self):
        return self.value.name()

    def get_type(self):
        print("CALLER:", inspect.stack()[1][3])
        print("ATTRIBUTE:", self.value)
        print(self.context)
        raise AttributeError("'PyAttribute' object has no attribute 'get_type'")


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

    def analyse(self):
        print("""
**********************************************************************
**********************************************************************
**********************************************************************
**********************************************************************
""")
        raise Exception("HERE")

    def name(self):
        return [ self.expression.name(), self.attribute.name() ]

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


