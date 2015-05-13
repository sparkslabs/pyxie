#!/usr/bin/python
#
# Copyright 2015 Michael Sparks
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

import ply.yacc as yacc

from pyxie.model.pynode import *
from pyxie.parsing.lexer import tokens

#
# I was going to have a stack of contexts. Instead, I'll maintain
# a stack but allow them to point to their parent. This actually means
# all contexts actually form a graph - which is true. (Many local contexts can
# point at a parent context)
#
# This then allows looking in the current context, and then outwards.
#

class ContextLeakage(Exception):
    pass

class Context(object):
    def __init__(self, parent=None):
        self.names = {} # Stores the type against the name.
        self.parent = parent
    def store(self,name,value):
        print "Context.store NAME", name, "VALUE", value
        if name in self.names:
            print "WARNING: Name %s already exists in names, this may be OK. Storing value %s" % (repr(name), repr(value))
        self.names[name] = value
    def lookup(self, name):
        if name in self.names:
            return self.names[name]
        if self.parent:
            return self.parent(name)
        raise ContextLeakage("Cannot find name %s in current context stack" % name)

class Grammar(object):
    precedence = (
        ('right', 'MINUS'),
    )
    tokens = tokens
    def __init__(self, *args, **argd):
        super(Grammar, self).__init__(*args, **argd)
        self.context_stack = [] # Will be necessary for functions/classes/etc
        self.global_context = Context()
        self.curr_ctx = self.global_context # Initial context is the global context

    def p_error(self,p):
        print "Syntax error at", p

    def p_program(self, p):
        "program : statements"
        p[0] = PyProgram(p[1])

    def p_statements_1(self, p):
        "statements : statement"
        p[0] = PyStatements(p[1])

    def p_statements_2(self, p):
        "statements : statement statements"
        p[0] = PyStatements(p[1], p[2])

    def p_statement_1(self, p):
        "statement : assignment_statement EOL"
        p[0] = p[1]

    def p_statement_3(self, p):
        "statement : expression EOL"
        p[0] = PyExpressionStatement(p[1])

    def p_statement_2(self, p):
        "statement : print_statement EOL"
        p[0] = p[1]

    def p_print_statement_1(self, p):
        "print_statement : PRINT expr_list"
        p[0] = PyPrintStatement(p[2])

    def p_expr_list_1(self,p):
        "expr_list : expression"
        p[0] = PyExprList(p[1])

    def p_expr_list_2(self,p):
        "expr_list : expression COMMA expr_list"
        p[0] = PyExprList(p[1],p[3])


    def p_assignment_statement(self, p):
        "assignment_statement : IDENTIFIER ASSIGN expression"
        identifier = PyIdentifier(self.curr_ctx, p.lineno(1), p[1])
        self.curr_ctx.store(p[1], identifier ) # Stuff into the current context

        p[0] = PyAssignment(identifier, p[3], p[2])

    def p_expression_1(self, p):
        "expression : arith_expression"
        p[0] = p[1]

    def p_expression_2(self, p):
        "expression : arith_expression PLUS expression"
        p[0] = PyPlusOperator(p[1],p[3])

    def p_expression_3(self, p):
        "expression : arith_expression MINUS expression"
        p[0] = PyMinusOperator(p[1],p[3])

    def p_expression_4(self, p):
        "expression : arith_expression POWER expression"
        p[0] = PyPowerOperator(p[1],p[3])

    def p_arith_expression_1(self, p):
        "arith_expression     : expression_atom"
        p[0] = p[1]

    def p_arith_expression_2(self, p):
        "arith_expression     : expression_atom TIMES arith_expression"
        p[0] = PyTimesOperator(p[1],p[3])

    def p_arith_expression_3(self, p):
        "arith_expression     : expression_atom DIVIDE arith_expression"
        p[0] = PyDivideOperator(p[1],p[3])

    def p_expression_atom_1(self, p):
        "expression_atom : value_literal"
        p[0] = p[1]

    ### Core Literals

    def p_value_literal_0(self, p):
        "value_literal : number"
        p[0] = p[1]

    def p_value_literal_1(self, p):
        "number : NUMBER"
        p[0] = PyInteger(p.lineno(1), p[1])

    def p_value_literal_2(self, p):
        "number : FLOAT"
        p[0] = PyFloat(p.lineno(1), p[1])

    def p_value_literal_3(self, p):
        "number : HEX"
        p[0] = PyHex(p.lineno(1), p[1])

    def p_value_literal_4(self, p):
        "number : OCTAL"
        p[0] = PyOctal(p.lineno(1), p[1])

    def p_value_literal_5(self, p):
        "number : BINARY"
        p[0] = PyBinary(p.lineno(1), p[1])

    def p_value_literal_5a(self,p):
        "number : MINUS number"
        p[0] = p[2].negate()

    def p_value_literal_6(self, p):
        "value_literal : STRING"
        p[0] = PyString(p.lineno(1), p[1])

    def p_value_literal_6a(self, p):
        "value_literal : CHARACTER"
        p[0] = PyCharacter(p.lineno(1), p[1])

    def p_value_literal_7(self, p):
        "value_literal : BOOLEAN"
        p[0] = PyBoolean(p.lineno(1), p[1])

    def p_value_literal_8(self, p):
        "value_literal : IDENTIFIER"
        p[0] = PyIdentifier(self.curr_ctx, p.lineno(1), p[1])
        self.curr_ctx.store(p[1], p[0]) # Stuff into the current context

def parse(source,lexer):

   if not source.endswith("\n"): # Be relaxed about end of file
       source = source+ "\n"

   yacc.yacc(module=Grammar())
   result = yacc.parse(source, lexer=lexer)
   return result
