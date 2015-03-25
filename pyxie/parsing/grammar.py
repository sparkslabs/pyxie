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
        """statement : NUMBER EOL
                     | FLOAT EOL
                     | HEX EOL
                     | OCTAL EOL
                     | BINARY EOL
                     | STRING EOL
                     | BOOLEAN EOL
                     """
        p[0] = [ "statement", p[1] ]

def parse(source,lexer):
   yacc.yacc(module=Grammar())
   result = yacc.parse(source, lexer=lexer)
   return result
