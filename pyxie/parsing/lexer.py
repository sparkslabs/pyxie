#!/usr/bin/python

import ply

# ------------------------------------------------------------
import ply.lex as lex


keywords = [ "True", "False" ]

tokens = [
   'NUMBER',
   'FLOAT',
   'HEX',
   'OCTAL',
   'BINARY',
   'STRING',
   'IDENTIFIER',
   'BOOLEAN',
   'EOL'
]

tokens += [ x.upper() for x in keywords ]

## Regular expression rules for simple tokens
#t_PLUS    = r'\+'
#t_MINUS   = r'-'
#t_TIMES   = r'\*'
#t_DIVIDE  = r'/'
#t_LPAREN  = r'\('
#t_RPAREN  = r'\)'


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in keywords:
        t.type = t.value.upper()
        if t.type == "TRUE" or t.type == "FALSE":
            t.type = "BOOLEAN"
            t.value = True if t.value == "True" else False
    return t

def t_SQUOTESTRING(t):
    r"'([^\\']|(\\.))*'"
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\\'', '\'')
    t.type = "STRING"
    return t

def t_DQUOTESTRING(t):
    r'"([^\\"]|(\\.))*"'
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\\"', '\"')
    t.type = "STRING"
    return t

# A regular expression rule with some action code
def t_BINARY(t):
    r'0b\d+'
    t.value = int(t.value,2)
    return t

def t_OCTAL(t):
    r'0o\d+'
    t.value = int(t.value,8)
    return t

def t_HEX(t):
    r'0x([abcdef]|\d)+'
    t.value = int(t.value,16)
    return t

def t_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Define a rule so we can track line numbers
def t_EOL(t):
    r'\n+'
    t.lexer.lineno += len(t.value)
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()
