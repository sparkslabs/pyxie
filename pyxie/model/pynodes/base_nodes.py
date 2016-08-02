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

# from pyxie.model.tree import Tree

# class PyNode(Tree):
class PyNode(object):
    """Representation of a python node"""
    tag = "node"
    ntype = None # Type for this node
    def __init__(self, *args):
        # Initialise the tree
        self.children = [] # Children are ordered
#        super(PyNode,self).__init__()

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

