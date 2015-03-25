#!/usr/bin/python

import ply.yacc as yacc

from pyxie.parsing.lexer import tokens

class Grammar(object):
    tokens = tokens
    def p_error(self,p):
        print "Syntax error at", p

    def p_program(self, p):
        "program : statements"
        p[0] = [ "program", p[1] ]

    def p_statements_1(self, p):
        "statements : statement"
        p[0] = [ "statements", [ p[1] ]]

    def p_statements_2(self, p):
        "statements : statement statements"
        p[0] = [ "statements", [ p[1] ] + p[2][1] ]

    def p_statement_1(self, p):
        "statement : value_literal EOL"
        p[0] = [ "statement", p[1] ]



    def p_value_literal_1(self, p):
        "value_literal : NUMBER"
        p[0] = [ "value_literal", p[1], "NUMBER", "INT", p.lineno(1) ]

    def p_value_literal_2(self, p):
        "value_literal : FLOAT"
        p[0] = [ "value_literal", p[1], "FLOAT", p.lineno(1) ]

    def p_value_literal_3(self, p):
        "value_literal : HEX"
        p[0] = [ "value_literal", p[1], "NUMBER", "HEX", p.lineno(1) ]

    def p_value_literal_4(self, p):
        "value_literal : OCTAL"
        p[0] = [ "value_literal", p[1], "NUMBER", "OCTAL", p.lineno(1) ]

    def p_value_literal_5(self, p):
        "value_literal : BINARY"
        p[0] = [ "value_literal", p[1], "NUMBER", "BINARY", p.lineno(1) ]

    def p_value_literal_6(self, p):
        "value_literal : STRING"
        p[0] = [ "value_literal", p[1], "STRING", p.lineno(1) ]

    def p_value_literal_7(self, p):
        "value_literal : BOOLEAN"
        p[0] = [ "value_literal", p[1], "BOOLEAN", "INT", p.lineno(1) ]





def parse(source,lexer):
   yacc.yacc(module=Grammar())
   result = yacc.parse(source, lexer=lexer)
   return result
