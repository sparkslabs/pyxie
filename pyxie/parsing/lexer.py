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

import ply

# ------------------------------------------------------------
import ply.lex as lex


keywords = [ "True", "False","print" ]

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
symbols = [ "ASSIGN", "COMMA" ]

tokens += [ x.upper() for x in keywords if (x not in [ "True", "False" ])]
tokens += symbols

## Regular expression rules for simple tokens
#t_PLUS    = r'\+'
#t_MINUS   = r'-'
#t_TIMES   = r'\*'
#t_DIVIDE  = r'/'
#t_LPAREN  = r'\('
#t_RPAREN  = r'\)'

t_ASSIGN = r'='
t_COMMA = r','

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    if t.value in keywords:
        if t.value in ["True", "False"]:
            t.type = "BOOLEAN"
            t.value = True if t.value == "True" else False
        else:
            t.type = t.value.upper()
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
