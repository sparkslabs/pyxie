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

from __future__ import print_function
from __future__ import absolute_import

import sys
import json

# These imports are pretty icky, but appropriate in this context

from .util import *
from .base_nodes import *
from .statements import *
from .operators import *
from .structural import *
from .values import *

MULTI_TYPES_WARN = False
WARNINGS_ARE_FAILURES = False


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
