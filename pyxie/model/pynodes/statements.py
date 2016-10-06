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
from .base_nodes import PyStatement
from .values import PyAttributeAccess

from pyxie.model.functions import builtins
from pyxie.model.functions import arduino_profile_function_calls as arduino


class PyAssignment(PyStatement):
    tag = "assignment_statement"
    def __init__(self, lvalue, rvalue, assign_type):
        super(PyAssignment,self).__init__()
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.assign_type = assign_type
        self.add_children(self.lvalue, self.rvalue)

    def __repr__(self):
        return "PyAssignment(%s,%s,%s)" % (repr(self.lvalue), repr(self.rvalue), repr(self.assign_type))

    def __json__(self):
        return [ self.tag, jdump(self.lvalue), jdump(self.rvalue), self.assign_type ]

    def __info__(self):
        info = super(PyAssignment, self).__info__()
        info[self.tag]["lvalue"] = self.lvalue.__info__()
        info[self.tag]["rvalue"] = self.rvalue.__info__()
        info[self.tag]["assign_type"] = self.assign_type
        return info

    def analyse(self):
        print("ANALYSING ASSIGNMENT")
        print("ANALYSE RIGHT")
        self.rvalue.analyse()
        self.lvalue.add_rvalue(self.rvalue)
        self.lvalue.analyse()

        self.ntype = self.get_type()

    def get_type(self):
        ltype = self.lvalue.get_type()
        rtype = self.rvalue.get_type()

        print("Type for lvalue:", ltype)
        print("Type for rvalue:", rtype)
        print("Types match:", rtype==ltype)

        # rtype wins because it's being used to set the left
        return rtype


class PyExpressionStatement(PyStatement):
    tag = "expression_statement"
    def __init__(self, value):
        super(PyExpressionStatement,self).__init__()
        self.value = value
        self.add_children(value)

    def __repr__(self):
        return "PyExpressionStatement(%s)" % (repr(self.value), )

    def __json__(self):
        return [ self.tag, jdump(self.value) ]

    def __info__(self):
        info = super(PyExpressionStatement, self).__info__()
        info[self.tag]["value"] = self.value.__info__()
        return info

    def analyse(self):
        with log.dent("PyExpressionStatement.analyse"):
            log.print("ANALYSING EXPRESSION STATEMENT")
            log.print("ANALYSING EXPRESSION STATEMENT", self)
            log.print("----------------------------->",self.value)
            try:
                self.value.analyse()
            except AttributeError:
                log.print("CANNOT ANALYSE VALUE")
                log.print(repr(self.value))
                log.print(jdump(self.value))
                raise
            self.ntype = self.get_type()

    def get_type(self):
        return self.value.get_type()


class PyFunctionCall(PyStatement):
    tag = "function_call"
    def __init__(self, func_label, expr_list):
        super(PyFunctionCall,self).__init__()
        self.func_label = func_label
        self.expr_list = expr_list
        if expr_list:
            self.add_children(expr_list)
        self.builtin = False
        self.arduino = False
        self.isiterator = False

    def __repr__(self):
        if self.expr_list:
            return "PyFunctionCall(%s, %s)" % (repr(self.func_label), repr(self.expr_list), )
        else:
            return "PyFunctionCall(%s)" % (repr(self.func_label), )

    def __json__(self):
        if self.expr_list:
            return [ self.tag, jdump(self.func_label), jdump(self.expr_list) ]
        else:
            return [ self.tag, jdump(self.func_label) ]

    def __info__(self):
        info = super(PyFunctionCall, self).__info__()
        info[self.tag]["name"] = self.func_label.__info__()
        if self.expr_list:
            info[self.tag]["args"] = [ x.__info__() for x in self.expr_list ]
        else:
            info[self.tag]["args"] = []
        return info

    def analyse(self):
        """
        FUNDAMENTAL PROBELM HERE IS RUMMAGEING AROUND INSIDE THE callable
        RATHER THAN ASKING THE CALLABLE WHAT TO DO.
        """
        func_name = self.func_label.name()

        #if type(func_name) == list:
        if type(self.func_label) == PyAttributeAccess:
            log.print("OK, name is:", func_name)
            log.print("HMMM:", dir(self))
            log.print("HMMM:", self.arduino)
            log.print("HMMM:", self.builtin)
            log.print("HMMM:", self.func_label)
            return
            raise NotImplementedError("Not yet implemented attribute access")

        if func_name in builtins:
            self.builtin = True
            self.ntype = self.get_type()
            return

        if func_name in arduino:
            self.arduino = True
            self.ntype = self.get_type()
            return

        return

    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        if self.builtin:
            meta = builtins[self.func_label.value]
            self.isiterator = meta.get("iterator", False)
            if self.isiterator:
                return meta.get("values_type", None)
            return meta.get("return_type", None)
        if self.arduino:
            meta = arduino[self.func_label.value]
            print("META META META", meta)
            print("META META META2", meta.get("return_ctype", None))
            return meta.get("return_ctype", None)

        return None


class PyForLoop(PyStatement):
    tag = "for_statement"
    def __init__(self, identifier, expression, block):
        super(PyForLoop,self).__init__()
        self.identifier= identifier
        self.expression = expression
        self.block = block
        self.add_children(identifier, expression, block)

    def __repr__(self):
        return "PyForLoop(%s, %s, %s)" % (repr(self.identifier), repr(self.expression), repr(self.block) )

    def __json__(self):
        return [ self.tag, jdump(self.identifier), jdump(self.expression), jdump(self.block) ]

    def __info__(self):
        info = super(PyForLoop, self).__info__()
        info[self.tag]["identifier"] = self.identifier.__info__()
        info[self.tag]["block"] = self.block.__info__()
        info[self.tag]["expression"] = self.expression.__info__()
        return info

    def analyse(self):
        # We'll need to decorate the function call with information from somewhere
        # For now though, we won't
        print("ANALYSING FOOR LOOP")
        print("                ... Analyse expression")
        expression = self.expression
        expression.analyse()
        print(expression)
        if expression.isiterator:
            print("Expression is an iterator")

        self.identifier.add_rvalue(expression) # The result of the expression becomes a repeated rvalue for the identifier, so this sorta makes sense

        print("                ... Update identifier")
        print("                ... Analyse identifier")
        self.identifier.analyse()

        print("                ... Analyse block")
        self.block.analyse()
        return


class PyWhileStatement(PyStatement):
    tag = "while_statement"
    def __init__(self, condition, block):
        super(PyWhileStatement,self).__init__()
        self.condition = condition
        self.block = block
        self.add_children(condition, block)

    def __repr__(self):
        return "PyWhileStatement(%s, %s)" % (repr(self.condition), repr(self.block) )

    def __json__(self):
        return [ self.tag, jdump(self.condition), jdump(self.block) ]

    def __info__(self):
        info = super(PyWhileStatement, self).__info__()
        info[self.tag]["condition"] = self.condition.__info__()
        # info[self.tag]["block"] = [ x.__info__() for x in self.expr_list ]
        info[self.tag]["block"] = self.block.__info__()
        return info

    def analyse(self):
        # We'll need to decorate the function call with information from somewhere
        # For now though, we won't
        print("ANALYSING WHILE BLOCK")
        print("analyse expression, and analyse block")
        self.condition.analyse()
        self.block.analyse()
        return

    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        print("GETTING WHILE BLOCK TYPE - which should be None - for now")
        return None


class PyIfStatement(PyStatement):
    tag = "if_statement"
    def __init__(self, condition, block, else_clause=None):
        super(PyIfStatement,self).__init__()
        self.condition = condition
        self.block = block
        self.else_clause = else_clause
        self.add_children(condition, block)

    def __repr__(self):
        else_clause = ""
        if self.else_clause:
            else_clause = ", %s" % (repr(self.else_clause),)
        return "PyIfStatement(%s, %s%s)" % (repr(self.condition), repr(self.block), else_clause)

    def __json__(self):
        else_clause = ""
        if self.else_clause:
            else_clause = jdump(self.else_clause)
        return [ self.tag, jdump(self.condition), jdump(self.block), "", else_clause ] # Space left for elif chain...

    def __info__(self):
        info = super(PyIfStatement, self).__info__()
        info[self.tag]["condition"] = self.condition.__info__()
        info[self.tag]["block"] = self.block.__info__()
        if self.else_clause:
            info[self.tag]["else_clause"] = self.else_clause.__info__()
        return info

    def analyse(self):
        print("ANALYSING IF BLOCK")
        print("analyse expression, and analyse block")
        self.condition.analyse()
        self.block.analyse()
        if self.else_clause:
            self.else_clause.analyse()
        return

    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        print("GETTING IF BLOCK TYPE - which should be None - for now")
        return None


class PyElIfClause(PyStatement):
    tag = "elif_clause"
    def __init__(self, condition, block, else_clause=None):
        super(PyElIfClause,self).__init__()
        self.condition = condition
        self.block = block
        self.else_clause = else_clause
        self.add_children(condition, block)

    def __repr__(self):
        else_clause = ""
        if self.else_clause:
            else_clause = ", %s" % (repr(self.else_clause),)
        return "PyElIfClause(%s, %s%s)" % (repr(self.condition), repr(self.block), else_clause)

    def __json__(self):
        else_clause = ""
        if self.else_clause:
            else_clause = jdump(self.else_clause)
        return [ self.tag, jdump(self.condition), jdump(self.block), "", else_clause ] # Space left for elif chain...

    def __info__(self):
        info = super(PyElIfClause, self).__info__()
        info[self.tag]["condition"] = self.condition.__info__()
        info[self.tag]["block"] = self.block.__info__()
        if self.else_clause:
            info[self.tag]["else_clause"] = self.else_clause.__info__()
        return info

    def analyse(self):
        print("ANALYSING ELIF BLOCK")
        print("analyse expression, and analyse block")
        self.condition.analyse()
        self.block.analyse()
        if self.else_clause:
            self.else_clause.analyse()
        return

    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        print("GETTING IF BLOCK TYPE - which should be None - for now")
        return None


class PyElseClause(PyStatement):
    tag = "else_clause"
    def __init__(self, block):
        super(PyElseClause,self).__init__()
        self.block = block
        self.add_children(block)

    def __repr__(self):
        return "PyElseClause(%s)" % (repr(self.block), )

    def __json__(self):
        return [ self.tag, jdump(self.block) ]

    def __info__(self):
        info = super(PyElseClause, self).__info__()
        info[self.tag]["block"] = self.block.__info__()
        return info

    def analyse(self):
        print("ANALYSING ELSE CLAUSE")
        print("analyse expression, and analyse block")
        self.block.analyse()
        return

    def get_type(self):
        # function calls have no default value, so for now we'll return None
        # This will be improved later on.
        print("GETTING ELSE CLAUSE TYPE - which should be None - for now")
        return None


class PyEmptyStatement(PyStatement):
    tag = "empty_statement"
    def __init__(self):
        super(PyEmptyStatement,self).__init__()

    def analyse(self):
        pass

    def __json__(self):
        return [ self.tag ]


class PyPassStatement(PyStatement):
    tag = "pass_statement"
    def __init__(self):
        super(PyPassStatement,self).__init__()

    def analyse(self):
        pass

    def __json__(self):
        return [ self.tag ]


class PyBreakStatement(PyStatement):
    tag = "break_statement"
    def __init__(self):
        super(PyBreakStatement,self).__init__()

    def analyse(self):
        pass

    def __json__(self):
        return [ self.tag ]


class PyContinueStatement(PyStatement):
    tag = "continue_statement"
    def __init__(self):
        super(PyContinueStatement,self).__init__()

    def analyse(self):
        pass

    def __json__(self):
        return [ self.tag ]

# DISABLED, due to removal of print statement in favour of print function
# DISABLED, LEFT IN CODE TO ASSIST WITH yield implementation later.
#
#class PyPrintStatement(PyStatement):
#    tag = "print_statement"
#    def __init__(self, expr_list):
#        super(PyPrintStatement,self).__init__()
#        self.expr_list = expr_list
#        self.add_children(expr_list)
#
#    def __repr__(self):
#        return "PyPrintStatement(%s)" % (repr(self.expr_list), )
#
#    def __json__(self):
#        return [ self.tag, jdump(self.expr_list) ]
#
#    def __info__(self):
#       info = super(PyPrintStatement, self).__info__()
#       info[self.tag]["args"] = [ x.__info__() for x in self.expr_list ]
#       return info
#
#    def analyse(self):
#        print("ANALYSING PRINT STATEMENT")
#        for expr in self.expr_list:
#            expr.analyse() # Descend through the tree
#
#        self.ntype = self.get_type()
#
#    def get_type(self):
#        # Print statement has no return value or default value
#        return None
