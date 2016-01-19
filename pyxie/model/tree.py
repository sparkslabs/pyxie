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
# Tree node to be used by the pynodes. Possibly other nodes later.
# Added once the pynode parsing required it.
#

def cmp_first(x,y):
    hx,tx = x
    hy,ty = y
    return cmp(hx,hy)

class Tree(object):
    def __init__(self):
        self.children = [] # Children are ordered

    def __pson__(self):
        return { "nId" : str(id(self)),
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

def _run_tests():
    "Basic smoke tests for the tree type"
    class Node(Tree):
        def __init__(self, tag):
            self.tag = tag
            super(Node, self).__init__()
        def info(self):
            return {"tag" : self.tag }

        def DF_walk(self):
            "Process the tree depth first"
            for i in self.depth_walk():
                print("DFS", i)

        def BF_walk(self):
            "Process the tree breadth first"
            for i in a.breadth_walk():
                print("BFS", i)

        def BFUP_walk(self):
            "Process the tree breadth first"
            for i in a.breadth_walk_up():
                print("BFUP", i)

        def __repr__(self):
            return "N:" + str(self.tag)

    # Build the following tree:
    #
    #                 A1                        1
    #       B2                  C3              2
    #   D4       E5        F6        G7         3
    #  H8 I9   J10 K11   L12 M13   N14 O15      4
    # P16                                Q17     5
    #    R18                                S19  6
    #
    a = Node(1)
    b = Node(2)
    c = Node(3)
    d = Node(4)
    e = Node(5)
    f = Node(6)
    g = Node(7)

    h = Node(8)
    i = Node(9)
    j = Node(10)
    k = Node(11)
    l = Node(12)
    m = Node(13)
    n = Node(14)
    o = Node(15)

    p = Node(16)
    q = Node(17)
    r = Node(18)
    s = Node(19)

    h.add_children(p)
    p.add_children(r)
    o.add_children(q)
    q.add_children(s)


    a.add_children(b,c)
    b.add_children(d,e)
    c.add_children(f,g)
    d.add_children(h,i)
    e.add_children(j,k)
    f.add_children(l,m)
    g.add_children(n,o)

    print("df_walk")
    a.DF_walk()

    print("bf_walk")
    a.BF_walk()

    print("bfup_walk")
    a.BFUP_walk()



if __name__ == "__main__":
    _run_tests()
