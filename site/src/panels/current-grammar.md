---
template: mainpanel
source_form: markdown
name: Pyxie Grammar
updated: Aug 2015
reviewed: 2 Aug 2015
title: Current Grammar support by Pyxie
---
    program : statements
    statements : statement
               | statement statements

    statement_block : INDENT statements DEDENT

    statement : assignment_statement
              | print_statement
              | general_expression
              | EOL
              | while_statement
              | break_statement
              | continue_statement
              | pass_statement
              | if_statement
              | for_statement

    assignment_statement -> IDENTIFIER ASSIGN general_expression # ASSIGN is currently limited to "="

    while_statement : WHILE general_expression COLON EOL statement_block

    break_statement : BREAK

    pass_statement : PASS

    continue_statement : CONTINUE

    if_statement : IF general_expression COLON EOL statement_block
                 | IF general_expression COLON EOL statement_block extended_if_clauses

    extended_if_clauses : else_clause
                        | elif_clause

    else_clause : ELSE COLON EOL statement_block

    elif_clause : ELIF general_expression COLON EOL statement_block
                | ELIF general_expression COLON EOL statement_block extended_if_clauses

    print_statement : 'print' expr_list # Temporary - to be replaced by python 3 style function

    for_statement | FOR IDENTIFIER IN general_expression COLON EOL statement_block

    expr_list : general_expression
              | general_expression COMMA expr_list

    general_expression : boolean_expression

    boolean_expression : boolean_and_expression
                       | boolean_expression OR boolean_and_expression

    boolean_and_expression : boolean_not_expression
                           | boolean_and_expression AND boolean_not_expression

    boolean_not_expression : relational_expression
                           | NOT boolean_not_expression

    relational_expression : expression
                          | relational_expression COMPARISON_OPERATOR expression

    expression : arith_expression
               | expression '+' arith_expression
               | expression '-' arith_expression
               | expression '**' arith_expression

    arith_expression : negatable_expression_atom
                     | arith_expression '*' negatable_expression_atom
                     | arith_expression '/' negatable_expression_atom


    negatable_expression_atom : "-" negatable_expression_atom 
                              | expression_atom

    expression_atom : value_literal
                    | IDENTIFIER '(' ')' # Function call, with no arguments
                    | IDENTIFIER '(' expr_list ')' # Function call
                    | '(' general_expression ')'

    value_literal : number
                  | STRING
                  | CHARACTER
                  | BOOLEAN
                  | IDENTIFIER

    number : NUMBER
           | FLOAT
           | HEX
           | OCTAL
           | BINARY
           | LONG         (suffice is L)
           | UNSIGNEDLONG (suffice is l)
           | '-' number

Current Lexing rules used by the grammar:

    NUMBER : \d+
    FLOAT : \d+.\d+ # different from normal python, which allows .1 and 1.
    HEX : 0x([abcdef]|\d)+
    OCTAL : 0o\d+
    BINARY : 0b\d+
    STRING - "([^\"]|\.)*" or '([^\']|\.)*' # single/double quote strings, with escaped values
    CHARACTER : c'.' /  c"." # Simplification - can be an escaped character
    BOOLEAN : True|False
    IDENTIFIER : [a-zA-Z_][a-zA-Z0-9_]*
