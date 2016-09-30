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
from .base_nodes import PyNode
from .statements import PyEmptyStatement

from pyxie.parsing.context import Context

class PyProgram(PyNode):
    tag = "program"
    def __init__(self, statements):
        super(PyProgram,self).__init__()
        self.statements = statements
        self.includes = None
        self.add_children(statements)
        self.context = Context() # Global context
        self.context.tag = self.tag

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
        # Add global context to child nodes before we start the analysis
        for child in self.children:
            child.add_context(self.context)

        self.ntype = self.get_type()
        self.statements.analyse() # Descend through the tree

        # print("CONTEXT: ================================================================================")
        # import pprint
        # pprint.pprint(self.context.__json__())
        # print("CONTEXT: ================================================================================")

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
        return info

    def analyse(self):
        print("ANALYSING BLOCK")
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

