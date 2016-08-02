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

# Utility functions

from __future__ import print_function
from __future__ import absolute_import

from contextlib import contextmanager

class indenting_logger(object):
    """
    This class exists specifically to help with debugging semantic analysis

    It's specifically meant to be used like this:
        with log.dent("PyExpressionStatement.analyse"):
            log.print("ANALYSING EXPRESSION STATEMENT")
            with log.dent("Some nested thing"):
               log.print("ANALYSING EXPRESSION STATEMENT", self)
               log.print("----------------------------->",self.value)

    """
    def __init__(self):
        self.indent = 0
    #
    def print(self,*argv):
        print(self.indent*"  " +  " ".join([str(x) for x in argv]) )
    #
    @contextmanager
    def dent(self,*argv):
        self.print("ENTER> " + " ".join([str(x) for x in argv]))
        self.indent += 1
        yield self
        self.indent -= 1

log = indenting_logger()


def jdump(thing):
    "Calls __json__ on a thing to try and convert it into a json serialisable thing"
    try:
        return thing.__json__()
    except AttributeError:
        print("WARNING::", repr(thing), "is not a pynode")
        print("       ::", type(thing))


def warn(message):
    if WARNINGS_ARE_FAILURES:
        raise Exception(message)
    else:
        print(message)

def depth_walk(root_node):
    "Return a generator that is a depth first walk of the tree"
    for node in root_node.children:
        for child in depth_walk(node):
            yield child
    yield root_node
