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

from .util import *
from .base_nodes import PyOperation

# This lookup should probably really look somewhere else
expression_mixed_types = {
       #(function_tag, type, type ) -> result_type
        ("op_times", "integer", "string") : "string",
        ("op_times", "string","integer") : "string",
        ("op_times", "integer", "char") : "string",
        ("op_times", "char","integer") : "string",
     }


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
            print("TAG", self.tag)
            print("ARG1", self.arg1.get_type())
            print("ARG2", self.arg2.get_type())
            raise

    def __repr__(self):
        return "%s(%s, %s)" % (self.classname(),repr(self.arg1),repr(self.arg2))

    def __json__(self):
        return [ self.tag, jdump(self.arg1), jdump(self.arg2) ]

    def get_type(self):
        return self.type

    def analyse(self):
        print("ANALYSING OPERATOR", self.tag)
        self.arg1.analyse()
        self.arg2.analyse()

        self.ntype = self.get_type()


class PyBoolOperator(PyOperation):
    tag = "base_bool_operator"

    @property
    def type(self):
        return "bool"

    def get_type(self):
        return "bool"

    def __init__(self, *argv):
        super(PyBoolOperator,self).__init__()
        self.argv = argv
        self.ntype = None
        self.add_children(*argv)

    def __info__(self):
        info = super(PyAndOperator, self).__info__()
        i = 1
        for arg in self.argv:
            info[self.tag]["arg%d" % i] = arg.__info__()
            i = i + 1
        return info

    def __repr__(self):
        return "%s%s" % (self.classname(),repr(tuple([x for x in self.argv])))

    def __json__(self):
        L = [ jdump(argv) for argv in self.argv ]
        return [ self.tag ] + L

    def analyse(self):
        print("ANALYSING OPERATOR:", self.tag)
        for arg in self.argv:
            arg.analyse()

        self.ntype = self.get_type()


class PyAndOperator(PyBoolOperator):
    tag = "and_operator"


class PyOrOperator(PyAndOperator):
    tag = "or_operator"


class PyNotOperator(PyBoolOperator):
    tag = "not_operator"


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


class PyComparisonOperator(PyOperation):
    tag = "comparison_operator"
    def __init__(self, comparison, arg1, arg2):
        super(PyComparisonOperator,self).__init__()
        self.comparison = comparison
        self.arg1 = arg1
        self.arg2 = arg2
        self.ntype = None
        self.add_children(arg1,arg2)

        print("CREATED COMPARISON OPERATOR", comparison, arg1, arg2)

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
        print("ANALYSING", self.tag)
        self.arg1.analyse()
        self.arg2.analyse()

        self.ntype = self.get_type()
