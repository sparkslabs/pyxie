---
template: mainpanel
source_form: markdown
name: Pyxie Grammar - Target
updated: July 2015
reviewed: 18 July 2015
title: Grammar support targetted by Pyxie
---
### Grammar todo

#### High Level

    program              : statements

    statements           : statement
                         | statement statements

    statement_block      : INDENT statements DEDENT

    statement            : EOL
                         | assignment_statement
                         | print_statement // This is really just a function call now
                         | general_expression  **[PARTIAL]**
                         | while_statement
                         | break_statement
                         | continue_statement
                         | if_statement
                         | for_statement
                         | import_statement  **[TBD]**
                         | class_statement  **[TBD]**
                         | def_statement  **[TBD]**
                         | return_statement  **[TBD]**
                         | yield_statement  **[TBD]**
                         | pass_statement  **[TBD]**

Note: general_expression  **[PARTIAL]** means we have parsing of general
expressions but not all types have appropriate functionality yet

Open question:

* try/except
* assert

(These are open questions because they are harder to implement on some levels,
assert would be useful though, but more useful if try/except were implemented)

### non-specific statements

NOTE: print is currently python 2 like, should be python 3 like.  Should be
made that once function calls are integrated.  In the meantime, printing
without having to implement general function calls is simpler.

    print_statement      : PRINT general_expression 
    pass_statement       : PASS  **[TBD]**

### Support for class definition  **[TBD]**

    class_statement      : CLASS PARENL ident_list PARENR COLON EOL class_block
    class_block          : INDENT class_statementlist DEDENT
    class_statementlist  : def_statement
                         | assignment_statement

### Support for function definition  **[TBD]**

    def_statement        : DEF identifier PARENL PARENR COLON EOL statement_block
                         | DEF identifier PARENL ident_list PARENR COLON EOL statement_block

    yield_statement      : YIELD general_expression

    return_statement     : RETURN
                         | RETURN general_expression

    ident_list           : identifier
                         | identifier COMMA ident_list

### Assignment Statement

    assignment_statement : identifier ASSIGN general_expression

### Namespace Functions  **[TBD]**

    import_statement     : FROM identifier IMPORT identifier
                         | IMPORT identifier

### Block Statements  **[WIP]**

#### Loops

All of these have been done - to a BARE level. That is:

* In for_statement general_expression is required to be an iterator function listed
  in pyxie.model.functions.builtins. This is currently just the function range with
  an interator implementation in clib. This is however the "correct" structure, not a
  sidestep.

* In while_statement this is a general expression expected to evaluate to a bool.

    for_statement        : FOR identifier IN general_expression COLON EOL statement_block

    while_statement      : WHILE general_expression COLON EOL statement_block

    break_statement      : BREAK
    continue_statement   : CONTINUE

#### Selection

    if_statement : IF general_expression COLON EOL statement_block
                 | IF general_expression COLON EOL statement_block extended_if_clauses

    extended_if_clauses : else_clause
                        | elif_clause

    elif_clause : ELIF general_expression COLON EOL statement_block
                | ELIF general_expression COLON EOL statement_block extended_if_clauses

    else_clause : ELSE COLON EOL statement_block

### Expressions involving sub-expressions

    general_expression : boolean_expression

    boolean_expression : boolean_and_expression
                       | boolean_expression OR boolean_and_expression

    boolean_and_expression : boolean_not_expression
                           | boolean_and_expression AND boolean_not_expression

    boolean_not_expression : relational_expression
                           | NOT boolean_not_expression

    relational_expression : relational_expression COMPARISON_OPERATOR expression
                          | expression

NOTE: Not all **types** are valid yet, and truthiness needs implementing

### Core Expressions  **[WIP]**

    expression           : arith_expression  **[WIP]**
                         | arith_expression PLUS expression
                         | arith_expression MINUS expression
                         | arith_expression POWER expression  **[TBD]**

    arith_expression     : expression_atom
                         | expression_atom TIMES arith_expression
                         | expression_atom DIVIDE arith_expression

    expression_atom      : value_literal
                         | func_call  **[PARTIAL]**
                         | PARENL general_expression PARENR

    value_literal        : number
                         | identifier
                         | string
                         | character
                         | boolean

Note: These are done for ints, floats, and for some strings. ("hello"+"world"
for example using std::string)

The lack of strings is why it's not listed as done

### Core Literals 

    number               : INTEGER
                         | FLOAT
                         | HEX
                         | OCTAL
                         | BINARY
                         | MINUS number

    string               : STRING

    character            : CHARACTER

    boolean              : TRUE | FALSE

    identifier : IDENTIFIER

### Function Calls   **[TBD]**

    func_call            : IDENTIFIER PARENL PARENR  **[TBD]**
                         | IDENTIFIER PARENL expr_list PARENR

    expr_list : general_expression
              | general_expression COMMA expr_list
