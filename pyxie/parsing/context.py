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

#
# I was going to have a stack of contexts. Instead, I'll maintain
# a stack but allow them to point to their parent. This actually means
# all contexts actually form a graph - which is true. (Many local contexts can
# point at a parent context)
#
# This then allows looking in the current context, and then outwards.
#
# A context is a collection of names inside a scope.
#
# Names that are bound within that scope can be well defined in that they bind to a
# literal value that has a type, or to the result of an expression which again has
# a clear derivable state.
#
# Names that are not bound into this state, by contrast are free variables.
# Free variables are not allows in little python at present, since they are potentially
# poly-typed
#
# While I can see my original point, having PyIdentifiers as the values here is kinda odd,
# since really the values associated with the names is the key point here, and the values
# are themselves more expression-result-types, not identifiers.
#
# As a result, contexts themselves need rework here
#
# Context Leakage is a very bad name.
#
# In fact, in any given context, an identifier gets assigned the results of an expression
# This may happen more than once.
#
# There are some problem scenarios:
#
#  * The results of two (or more) expressions assigned to a name are conflicting types
#  * An expression uses a name that is not yet well defined at that point in a program
#
# Suggests the following strategy:
#
#  * So, we should go through the program, assigning *expressions* to names in contexts
#  * When we need the type of an identifier, we look in it's context for the name, find
#    an expression and evaluate it's type


from __future__ import print_function
from __future__ import absolute_import

class UndefinedValue(Exception):
    pass

class Context(object):

    contexts = {}
    def __init__(self, parent=None):
        self.names = {} # Stores the type against the name.
        self.parent = parent
        if id(self) not in self.contexts:
            self.contexts[id(self)] = self

    def store(self, name, expression):
        print("Context.store NAME", name, "VALUE", expression)
        if name in self.names:
            print("WARNING: Name %s already exists in names, this may be OK. Storing expression %s" % (repr(name), repr(expression)))
        try:
            self.names[name].append( expression )
        except KeyError:
            self.names[name] = [ expression ]
        print("CONTEXT", self.names)

    def lookup(self, name):
        if name in self.names:
            values = self.names[name]
            return values[0]
        if self.parent:
            values = self.parent.lookup(name)
            return values[0]
        raise UndefinedValue("Cannot find name %s in current context stack" % name)

    def __repr__(self):
        return repr(id(self))

    def __json__(self):
        names_info = {}
        for name in self.names:
            if type(self.names[name]) == type(""):
                names_info[name] = self.names[name]
            else:
                names_info[name] = self.names[name] # .__info__()
        return {"id": id(self), "parent": id(self.parent) if self.parent is not None else None, "names": names_info}

