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


profile_context = None # REVIEW: Initial test location for a global profile context.

class Context(object):
    contexts = {}
    def __init__(self, parent=None):
        self.names = {} # Stores the type against the name.
        self.parent = parent
        self.tag = None  # Tag has been added to allow us to identify in what linguistic contruct this context has been created.
        if id(self) not in self.contexts:
            self.contexts[id(self)] = self

    def store(self, name, expression):
        print("Context.store NAME", name, repr(name), "VALUE", expression)
        if name in self.names:
            print("WARNING: Name %s already exists in names, this may be OK. Storing expression %s" % (repr(name), repr(expression)))
        try:
            self.names[name].append( expression )
        except KeyError:
            self.names[name] = [ expression ]
        print("CONTEXT", self.names)

    def complete_context(self):
        search_list = []
        search_list.append( ( self.tag, self.names ) )
        if self.parent:
            search_list = search_list + (self.parent.complete_context())
        else:
            if self != profile_context:
                # Don't recurse if at end
                search_list = search_list + (profile_context.complete_context())
        return search_list

    def lookup(self, name):
        print("Context.lookup -pc ", profile_context)
        if self.tag:
            print("Context.TAG ", self.tag)
        print("Context.lookup", name)

        print("Context.lookup",self.complete_context())
        if name in self.names:
            values = self.names[name]
            return values[0]
        if self.parent:
            values = self.parent.lookup(name)
            return values[0]
        if profile_context: # Check class global context
            if profile_context != self: # Check we're not recursing(!)
                try:
                    return profile_context.lookup(name)
                except UndefinedValue:
                    # We failed the lookup, so allow the final lookup to be the actual error
                    # So we deliberately suppress the lookup error here.
                    pass

        print(self.complete_context())
        raise UndefinedValue("Cannot find name %s in current context stack" % name, str(self.complete_context()) )

    def __str__(self):
        return str(self.__json__())

    def __repr__(self):
        return repr(id(self))

    def __json__(self):
        names_info = {}
        for name in self.names:
            if type(self.names[name]) == type(""):
                names_info[name] = self.names[name]
            else:
                names_info[name] = self.names[name] # .__info__()
        result = {}
        result["id"] = id(self)
        result["parent"] = id(self.parent) if self.parent is not None else None
        result["names"] =  names_info
        if profile_context:
            result["profile_context"] =  profile_context
        if self.tag:
            result["tag"] =  self.tag
        return result

