---
template: mainpanel
source_form: markdown
name: Pyxie Lexical analysis - Target
updated: July 2015
reviewed: 18 July 2015
title: Lexical analysis support targetted by Pyxie
---
### Lexical Analysis TODO

    Keywords: "and", "not", "or",
              "True", "False",
              "class", "def", "yield", "return",
              "while", "for", "in", "if", "elif", "else", "break", "continue",
              "from", "import",
              "pass",
              "print"

    Punctuation: ','  '('  ')'  ':'  '*'  '/'  '+'  '-'  '**' **[TBD]**
                 COMPARISON_OPERATOR      **[TBD]**
                 ASSIGN

    COMPARISON_OPERATOR: (<|>|==|>=|<=|<>|!=|in|not +in|is|is +not)
    ASSIGN: '='

    Structural: EOL INDENT DEDENT
        EOL -- Should be logical, actually '\n'
        INDENT -- emitted after increased number of leading spaces after EOL
        DEDENT -- emitted after decreased number of leading spaces after EOL

    Literals: IDENTIFIER NUMBER STRING
        IDENTIFIER:     [a-zA-Z_][a-zA-Z0-9_]*

        NUMBER: BINARY OCTAL HEX FLOAT INTEGER
            BINARY -- 0b\d+
            OCTAL -- 0o\d+
            HEX -- 0x([abcdef]|\d)+
            FLOAT -- \d+\.\d+
            INTEGER -- \d+

        STRING: DQUOTESTRING | SQUOTESTRING 
            DQUOTESTRING: "([^"]|.)*"
            SQUOTESTRING: '([^']|.)*'

        CHARACTER: SCHARACTER | DCHARACTER
            SCHARACTER: c'([^']|.)'
            DCHARACTER: c"([^"]|.)"

            I'm actually contemplating having b'<char>' instead, but that
            makes single character byte string tricky.  This will probably
            be revisited, but one thought is this: If a single character
            byte string is actually required, do this: b'C'+b'' - ie append
            an empty byte string.  The compiler will be special cased to
            detect this and force the expression to be the single bytestring
            b'C'. It's a bit icky, so for the moment I've added a character
            literal instead to see what works better.

            This isn't ideal, but it deals with the fact that often we do
            want to be able to deal with just characters C in embedded
            systems.
