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

from __future__ import print_function
from __future__ import absolute_import

import re
import ply

# ------------------------------------------------------------
import ply.lex as lex

states = (
        ('NORMAL',    'exclusive'), # Normal state for parsing
        ('BLOCKS',    'exclusive'), # Used for checking block structure - this is also our INITIAL state
        ('ENDBLOCKS', 'exclusive'), # Used for closing block structure
)

tabsize = 8

keywords = [ "and", "not", "or",
             "True", "False",
             "class", "def", "yield", "return",
             "while", "for", "in", "if", "elif", "else", "break", "continue",
             "from", "import",
             "pass",
#             "print"   # DISABLED, due to removal of print statement in favour of print function
#                       # DISABLED, LEFT IN CODE TO ASSIST WITH yield implementation later.
            ]

tokens = [
   'NUMBER',
   'INTEGER',
   'FLOAT',
   'HEX',
   'OCTAL',
   'BINARY',
   'STRING',
   'IDENTIFIER',
   'BOOLEAN',
   'CHARACTER',
   'UNSIGNEDLONG',
   'SIGNEDLONG'
   ]

punctuation = [ "COMMA", "PARENL", "PARENR", "COLON", "TIMES", "DIVIDE", "PLUS", "MINUS", "POWER", "DOT",
                "COMPARISON_OPERATOR",
                "ASSIGN"
              ]

structural = [ "EOL", "INDENT", "DEDENT" ]

tokens += [ x.upper() for x in keywords if (x not in [ "True", "False" ])]
tokens += punctuation
tokens += structural

## Regular expression rules for simple cases
t_NORMAL_COLON = r':'

t_NORMAL_PLUS    = r'\+'
t_NORMAL_MINUS   = r'-'
t_NORMAL_TIMES   = r'\*'
t_NORMAL_DIVIDE  = r'/'
t_NORMAL_POWER = r'\*\*'
t_NORMAL_PARENL = r'\('
t_NORMAL_PARENR = r'\)'

t_NORMAL_ASSIGN = r'='
t_NORMAL_COMMA = r','
t_NORMAL_COMPARISON_OPERATOR = r'(<>|==|>=|<=|!=|<|>|in|not +in|is|is +not)'

# Things ignored inside various states
t_NORMAL_ignore  = ' \t'
t_INITIAL_BLOCKS_ignore  = ''
t_ENDBLOCKS_ignore  = ''

def t_NORMAL_SCHARACTER(t):
    r"c'([^\\']|(\\.))'"
    t.value = t.value[2:-1]
    t.value = t.value.replace('\\\'', '\'')
    t.value = t.value.replace('\\\"', '\"')
    t.type = "CHARACTER"
    return t

def t_NORMAL_DCHARACTER(t):
    r'c"([^\\"]|(\\.))"'
    t.value = t.value[2:-1]
    t.value = t.value.replace('\\\'', '\'')
    t.value = t.value.replace('\\\"', '\"')
    t.type = "CHARACTER"
    return t

def t_NORMAL_UNSIGNEDLONG(t):
    r'\d+l'
    t.value = int(t.value[:-1])
    return t

def t_NORMAL_SIGNEDLONG(t):
    r'\d+L'
    t.value = int(t.value[:-1])
    return t

def t_NORMAL_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'

    if t.value in keywords:
        if t.value in ["True", "False"]:
            t.type = "BOOLEAN"
            t.value = True if t.value == "True" else False

        else:
            # Other keywords converted to token types
            t.type = t.value.upper()

    return t

def t_NORMAL_SQUOTESTRING(t):
    r"'([^\\']|(\\.))*'"
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\\'', '\'')
    t.type = "STRING"
    return t

def t_NORMAL_DQUOTESTRING(t):
    r'"([^\\"]|(\\.))*"'
    t.value = t.value[1:-1]
    t.value = t.value.replace('\\\"', '\"')
    t.type = "STRING"
    return t

# A regular expression rule with some action code
def t_NORMAL_BINARY(t):
    r'0b\d+'
    t.value = int(t.value,2)
    return t

def t_NORMAL_OCTAL(t):
    r'0o\d+'
    t.value = int(t.value,8)
    return t

def t_NORMAL_HEX(t):
    r'0x([abcdef]|\d)+'
    t.value = int(t.value,16)
    return t

def t_NORMAL_FLOAT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

t_NORMAL_DOT = r'\.'

def t_NORMAL_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Define a rule so we can track line numbers
def t_INITIAL_NORMAL_ENDBLOCKS_EOL(t):
    r'\n+'
    t.lexer.curr_indent = 0
    t.lexer.lineno += len(t.value)

    t.lexer.begin('BLOCKS') # We are always in BLOCKS state if we reach EOL

    return t

def t_BLOCKS_EOL(t):
    r'\n+'
    t.lexer.curr_indent = 0
    t.lexer.lineno += len(t.value)

    return t

def t_NORMAL_INCLUDELINE(t):
    r'\#include.*'
    print("WE SAW A #INCLUDE line! :-)")
    print("It was this:", repr(t.value))
    t.lexer.includes.append(t.value)

def t_INITIAL_BLOCKS_WS(t):
    r'[ \t]+'

    #
    # All leading whitepace on a line.
    #
    # This allows us to get the indent size. We don't emit any indent or dedent here though
    #
    count = 0
    for char in t.value:
      if char == " ":
          count += 1
      if char == "\t":
          count += tabsize

    t.lexer.curr_indent = count

def t_INITIAL_BLOCKS_INDENT(t):
    r'[^ \t\n]'

    #
    # Trigger on first non-whitespace character on the line
    #
    # Put it back in the lexer, because we don't want to consume it.
    t.lexer.lexpos -= 1

    # Decide whether to switch to ENDBLOCKS or NORMAL mode
    curr_indent = t.lexer.curr_indent
    dedents_needed = 0

    while t.lexer.indents[-1] > curr_indent:
        t.lexer.indents.pop()
        dedents_needed += 1

    if dedents_needed > 0:
        t.lexer.dedents_needed = dedents_needed
        t.lexer.begin('ENDBLOCKS')
        return

    # Not closing a block, so parsing inside a block

    # If it's a new one, add it to the "lexer.indents" stack
    if curr_indent > t.lexer.indents[-1]:
        t.lexer.indents.append(t.lexer.curr_indent)
        print("EMITTING INDENT", t)
        return t

    t.lexer.begin('NORMAL')

def t_ENDBLOCKS_DEDENT(t):
    r'.'

    # We use the lexer to re-call this function as many times as we need to
    # emit a DEDENT token
    #
    # We do this by decrementing our counter, and pushing back the token that
    # brought us here
    # When the counter reaches 0, we switch to the NORMAL state.
    #

    t.lexer.lexpos -= 1

    # This allows us to emit as many DEDENT tokens as necessary.
    if t.lexer.dedents_needed > 0:
        t.lexer.dedents_needed -= 1
        print("EMITTING DEDENT", t)
        return t
    t.lexer.begin('NORMAL')

# Error handling rule
def t_ANY_error(t):
    print("Illegal character '%s'" % t.value[0], t)
    t.lexer.skip(1)

def build_lexer():
    # Build the lexer
    lexer =  lex.lex(reflags=re.MULTILINE)
    lexer.includes = []
    lexer.lineno = 1
    lexer.curr_indent = 0
    lexer.indents = [0]
    return lexer

# lexer = build_lexer()

if __name__ == "__main__":

    lexer = build_lexer()
    # Test it out
    data = '''\
and not or
True False
class def yield return
while for in if elif else break continue
from import
pass
print

first = 1
second = 2
third = 3

if 1:
    print first, second, third

print 1, 2, "hello"
print 1, 2.1, 0x20, 0b10101, 0100, True, False, "hello"
print -1, -2.1, -0x20, -0b10101, -0100, True, False, "hello"
'''

    # Give the lexer some input
    lexer.input(data)

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
