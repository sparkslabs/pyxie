---
template: mainpage
source_form: markdown
name: PyNodes
updated: January 2016
reviewed: 26 January 2016
title: Representing Python Programs using PyNodes
skip: True
---
Representing Python Programs using PyNodes
==========================================
When the python program is parsed, the parser creates an AST using PyNodes. These PyNodes
represent various parts of the python program. In particular the semantics of the AST
is stored in objects that derive from a class called PyNode. PyNodes itself however
is a subclass of a Tree type which is used to provide basic tree structure.

At present this is more than a little confused because PyNode *also* constructs a tree
from attributes it presents, so something is clearly wrong there. This is in part due
to the increasing complexity of structures as Pyxie gets more complex, so this file is
to document the existing structure - based on a spreadsheet analysis - to aid with
simplification.

Tree Nodes have the following:
  * Attributes:
    * children = [] # default value
  * Methods:
    * __pson__ - returns a "Python structure object notation" representation of the tree.
                 This boils down to a structure based on:
                     { "nId" : str(id(self)),
                       "nStr" : str(self)[:40],
                       "nchildren" : [x.__pson__() for x in self.children] }
    #
    def add_child(self, node):
        self.children.append(node)
    #
    def add_children(self, *nodes):
        self.children = self.children + list(nodes)
    #
    def depth_walk(self):
        "Return a generator that is a depth first walk of the tree"
        for node in self.children:
            for child in node.depth_walk():
                yield child
        yield self

    def _breadth_walk_children(self,depth=2):
        nodes = []
        for node in self.children:
            nodes.append( (depth, node ) )

        for node in self.children:
            for cdepth, child in node._breadth_walk_children(depth+1):
                nodes.append( (cdepth, child ) )

        nodes.sort(cmp_first)
        for node in nodes:
            yield node

    def breadth_walk(self):
        "Return a generator that is a breadth first walk of the tree, not optimised, copes with unbalanced trees"
        yield self
        nodes = []
        for node in self._breadth_walk_children():
            nodes.append(node)

        nodes.sort(cmp_first)
        for depth, node in nodes:
            yield node

    def breadth_walk_up(self):
        "Return a generator that is a breadth first walk of the tree. Starts with lowest layers. Not optimised, copes with unbalanced trees"
        nodes = []
        for node in self._breadth_walk_children():
            nodes.append(node)

        nodes.sort(cmp_first)
        max_depth = 0
        for depth, node in nodes:
            if depth> max_depth:
                max_depth=depth

        for this_depth in range(max_depth,1,-1):
            for depth, node in nodes:
                if depth == this_depth:
                    yield node
        yield self
