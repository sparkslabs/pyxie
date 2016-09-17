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

class PyNode(object):
    """Representation of a python node"""
    tag = "node"
    ntype = None # Type for this node
    def __init__(self, *args):
        self.children = [] # Children are ordered
        self.context = None # Default to no context initially

    def add_context(self, context):
        # Default is to Inherit the context of the container of this
        # PyNode. Some pynodes may override this behaviour - in particular
        # this behaviour may be overridden in function definitions for
        # example, it will also be overridden by nodes with children
        self.context = context
        for child in self.children:
            child.add_context(context)

    def add_child(self, node):
        self.children.append(node)

    def add_children(self, *nodes):
        self.children = self.children + list(nodes)

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
