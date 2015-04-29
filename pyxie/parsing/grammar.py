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

from pyxie.parsing.lexer import tokens

class Grammar(object):
    precedence = (
        ('right', 'MINUS'),
    )
    tokens = tokens
    def p_error(self,p):
        print "Syntax error at", p

    def p_program(self, p):
        "program : statements"
        p[0] = [ "program", p[1] ]

    def p_statements_1(self, p):
        "statements : statement"
        p[0] = [ "statements", [ p[1][1] ]]

    def p_statements_2(self, p):
        "statements : statement statements"
        p[0] = [ "statements", [ p[1][1] ] + p[2][1] ]

    def p_statement_1(self, p):
        "statement : assignment_statement EOL"
        p[0] = [ "statement", p[1] ]

    def p_statement_2(self, p):
        "statement : print_statement EOL"
        p[0] = [ "statement", p[1] ]

    def p_print_statement_1(self, p):
        "print_statement : PRINT expr_list"
        p[0] = [ "print_statement", p[2][1] ]


    def p_expr_list_1(self,p):
        "expr_list : expression"
        p[0] = [ "expr_list", [ p[1] ] ]

    def p_expr_list_2(self,p):
        "expr_list : expression COMMA expr_list"
        p[0] = [ "expr_list", [ p[1] ] + p[3][1] ]

    def p_statement_3(self, p):
        "statement : expression EOL"
        p[0] = [ "statement", p[1] ]

    def p_assignment_statement(self, p):
        "assignment_statement : IDENTIFIER ASSIGN expression"
        p[0] = ["assignment_statement", [p[1], "IDENTIFIER", p.lineno(1) ],
                                        ["ASSIGN", p[2]],
                                        p[3]
               ]

    def p_expression_1(self, p):
        "expression : arith_expression"
        p[0] = p[1]

    def p_expression_2(self, p):
        "expression : arith_expression PLUS expression"
        p[0] = ["operator_function", "plus", p[1], p[3] ]

    def p_expression_3(self, p):
        "expression : arith_expression MINUS expression"
        p[0] = ["operator_function", "minus", p[1], p[3] ]

    def p_expression_4(self, p):
        "expression : arith_expression POWER expression"
        p[0] = ["operator_function", "power", p[1], p[3] ]

    def p_arith_expression_1(self, p):
        "arith_expression     : expression_atom"
        p[0] = p[1]

    def p_arith_expression_2(self, p):
        "arith_expression     : expression_atom TIMES arith_expression"
        p[0] = ["operator_function", "times", p[1], p[3] ]

    def p_arith_expression_3(self, p):
        "arith_expression     : expression_atom DIVIDE arith_expression"
        p[0] = ["operator_function", "divide", p[1], p[3] ]

    def p_expression_atom_1(self, p):
        "expression_atom : value_literal"
        p[0] = p[1]

    ### Core Literals

    def p_value_literal_0(self, p):
        "value_literal : number"
        p[0] = p[1]

    def p_value_literal_1(self, p):
        "number : NUMBER"
        p[0] = [ "value_literal", p[1], "NUMBER", "INT", p.lineno(1) ]

    def p_value_literal_2(self, p):
        "number : FLOAT"
        p[0] = [ "value_literal", p[1], "FLOAT", p.lineno(1) ]

    def p_value_literal_3(self, p):
        "number : HEX"
        p[0] = [ "value_literal", p[1], "NUMBER", "HEX", p.lineno(1) ]

    def p_value_literal_4(self, p):
        "number : OCTAL"
        p[0] = [ "value_literal", p[1], "NUMBER", "OCTAL", p.lineno(1) ]

    def p_value_literal_5(self, p):
        "number : BINARY"
        p[0] = [ "value_literal", p[1], "NUMBER", "BINARY", p.lineno(1) ]

    def p_value_literal_5a(self,p):
        "number : MINUS number"
        p[2][1] = -p[2][1]
        p[0] = p[2]

    def p_value_literal_6(self, p):
        "value_literal : STRING"
        p[0] = [ "value_literal", p[1], "STRING", p.lineno(1) ]

    def p_value_literal_6a(self, p):
        "value_literal : CHARACTER"
        p[0] = [ "value_literal", p[1], "CHARACTER", p.lineno(1) ]

    def p_value_literal_7(self, p):
        "value_literal : BOOLEAN"
        p[0] = [ "value_literal", p[1], "BOOLEAN", "INT", p.lineno(1) ]

    def p_value_literal_8(self, p):
        "value_literal : IDENTIFIER"
        p[0] = [ "value_literal", p[1], "IDENTIFIER", p.lineno(1) ]

def parse(source,lexer):

   if not source.endswith("\n"): # Be relaxed about end of file
       source = source+ "\n"

   yacc.yacc(module=Grammar())
   result = yacc.parse(source, lexer=lexer)
   return result
