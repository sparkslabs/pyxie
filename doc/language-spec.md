Little Python Language Spec
===========================

Little Python is a restricted subset of Python 3. (and 2.7)

**This is a work in progress.** The implementation does not yet match
this spec. As a result, the grammar may be bogus. You hopefully get the
idea though.

## Semi-formal syntactic language features todo:

### Built in types to be supported

Simple
* Numbers
* Strings
* Booleans

Harder
* NULL - Probably constrained **[TBD]**
* LISTS - Probably constrained **[TBD]**
* TUPLES - Probably constrained **[TBD]**
* DICTIONARIES - Probably constrained **[TBD]**
* Objects - classes **[TBD]**

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

        CHARACTER: b'[^']'  **[TBD]**
            If a single character byte string is actually required, do this: b'C'+b'' - ie append
            an empty byte string. The compiler will be special cased to detect this and force
            the expression to be the single bytestring b'C'

            This isn't ideal, but it deals with the fact that often we do want to be able to deal
            with just characters C in embedded systems.

### Grammar todo

#### High Level

    program              : statements

    statements           : statement
                         | statement statements

    block                : INDENT statements DEDENT

    statement            : EOL
                         | assignment_statement
                         | print_statement // This is really just a function call now
                         | fullexpression  **[TBD]**
                         | while_statement  **[TBD]**
                         | if_statement  **[TBD]**
                         | for_statement  **[TBD]**
                         | import_statement  **[TBD]**
                         | class_statement  **[TBD]**
                         | def_statement  **[TBD]**
                         | return_statement  **[TBD]**
                         | yield_statement  **[TBD]**
                         | pass_statement  **[TBD]**


### non-specific statements

print is currently python 2 like, should be python 3 like.
Should be made that once function calls are integrated.

    print_statement      : PRINT fullexpression 
    pass_statement       : PASS  **[TBD]**

### Support for class definition  **[TBD]**

    class_statement      : CLASS PARENL ident_list PARENR COLON EOL class_block
    class_block          : INDENT class_statementlist DEDENT
    class_statementlist  : def_statement
                         | assignment_statement

### Support for function definition  **[TBD]**

    def_statement        : DEF identifier PARENL PARENR COLON EOL block
                         | DEF identifier PARENL ident_list PARENR COLON EOL block

    yield_statement      : YIELD fullexpression

    return_statement     : RETURN
                         | RETURN fullexpression

    ident_list           : identifier
                         | identifier COMMA ident_list

### Assignment Statement

    assignment_statement : identifier ASSIGN fullexpression

### Namespace Functions  **[TBD]**

    import_statement     : FROM identifier IMPORT identifier
                         | IMPORT identifier

### Block Statements  **[TBD]**

#### Loops

    for_statement        : FOR identifier IN fullexpression COLON EOL block

    while_statement      : WHILE fullexpression COLON EOL block

#### Selection

    if_statement         : IF fullexpression COLON EOL block
                         | IF fullexpression COLON EOL block if_trailer

    if_trailer           : elif_clauses
                         | else_clause
    elif_clauses         : elif_clause
                         | elif_clause if_trailer
    elif_clause          : ELIF fullexpression COLON EOL block
    else_clause          : ELSE COLON EOL block


### Expressions involving sub-expressions  **[TBD]**

    fullexpression       : or_expression

    or_expression        : and_expression 
                         | and_expression OR or_expression

    and_expression       : not_expression
                         | not_expression AND not_expression

    not_expression       : comparison
                         | NOT not_expression

    comparison           : expression
                         | expression COMPARISON_OPERATOR expression

### Core Expressions

    expression           : arith_expression
                         | arith_expression TIMES expression
                         | arith_expression DIVIDE expression
                         | arith_expression POWER expression

    arith_expression     : expression_atom
                         | expression_atom PLUS arith_expression
                         | expression_atom MINUS arith_expression

    expression_atom      : value_literal
                         | func_call
                         | PARENL fullexpression PARENR

    value_literal        : number
                         | identifier
                         | string
                         | boolean

### Core Literals 

    number               : INTEGER
                         | FLOAT
                         | HEX
                         | OCTAL
                         | BINARY
                         | MINUS number

    string               : STRING

    boolean              : TRUE | FALSE

    identifier : IDENTIFIER

### Function Calls   **[TBD]**

    func_call            : IDENTIFIER PARENL PARENR
                         | IDENTIFIER PARENL expr_list PARENR

    expr_list : expression
              | expression COMMA expr_list



## Lexical Analysis Implementation

Lexical analyser has the following states:

* INITIAL - Starting state - actually the same as BLOCKS
* NORMAL - This is used for usual parsing rules
* BLOCKS - Switched into after we detect a newline - to allow injection of
  indents, and switching to dedent or code if appropriate. 
* ENDBLOCKS - Used for emitting sufficient dedents - contains just one rule,
  that either returns a dedent if needed or switches to CODE. Does not
  consume any tokens

## Informal todo list

* The parser is line oriented, should be logical lines   **[TBD]**
* Statements are separated by NEWLINES
* Block structure generates INDENT/DEDENT tokens
* Value literals: Integers, String, Boolean
* Identifiers
* basic assignment statements - ie identifer equals expression
* function calls with expressions as arguments  **[TBD]**
* function definitions with an optional argument list  **[TBD]**
* print statements  **[TBD]**
* expression statements  **[TBD]**
* expressions - specifically:  **[TBD]**
    * Those involving value literals, identifiers and function calls
    * Infix expressions involving * + / -
    * Parentheses ( ) for nested expressions.
* Loops - while / for**[TBD]**
    * forever_loop (while True)   **[TBD]**
    * while takes an expression for the condition   **[TBD]**
    * for takes an identifier for the iterator, and expression to be
      iterated over. The expression is treated as indexable thing with
      a length. A range() function call is detected and treated as a
      special case.   **[TBD]**
* If statements including elif and else clauses   **[TBD]**
* parsing of yield statements   **[TBD]**
* parsing of import statements, parsing of from...import... statements   **[TBD]**
* Expressions - bitwise operators, logical operators, boolean operators   **[TBD]**
* break / continue statements   **[TBD]**
* Lists, list literals   **[TBD]**
* doc strings   **[TBD]**
* comments   **[TBD]**
* Dictionaries, dictionary literals   **[TBD]**
* Objects / object attribute access   **[TBD]**
* return statement   **[TBD]**
* Lines are logical lines    **[TBD]**
 * ie Newlines are not yet suppressed.   **[TBD]**
 * Explicit line joining is not supported [2.1.5]    **[TBD]**
 * Implicitly line joining is not yet supported  [2.1.6]   **[TBD]**
* Comments are started with a # character [*]   **[TBD]**
* Generator implementation   **[TBD]**

## Language features NOT supported    **[TBC]**

Note: Operator precedence needs ironing out   **[TBD]**

* Encoding declarations are not supported. Files are UTF-8 only
* General assignment statements -
    * No unpacking of identifier lists - ie no x,y,z = <rhs>, nor x,(y,z) = <rhs>
    * No augmented assignment - eg no += -= *= and so on
* Generalised classes (classes are specifically limited here)
* No dynamic functions, classes
* No dynamic lists, dictionaries yet*
* exceptions - exception values; raise statements;  try, except, finally, else blocks. (maybe later)
* operators: ** (power), ~ (bitwise negation), modulo, //, string templates via modulo operator, shift operators, conditional expressions
* Line continuation: using parentheses, using string literal, for string concatenation
* function calls : named arguments, calling with *argv, **argd
* function definitions : optional arguments, named arguments, *argv, **ard
* redirected print statements
* generator expressions
* list/dictionary/set comprehensions, slices - not generally supported - just a subset
* tuples, sets - not generally supported - just a subset
* with statements
* decorators
* long integers, imaginary numbers
* backquoted string conversions
* variant string literal types. (include r'' strings)
* Escaped strings (for now)
* else clauses for while / for loops
* for does not support unpacking of iterated objects - ie for x,y,z in <thing> is not supported
* for does not support single line nesting (for x in y for y in z)
* yield expression parsing
* implementation of yield
* asserts, del statement
* importing modules, importing names from modules, relative imports
* future statements
* exec statement, eval expressions
* global statements, nonlocal statements
* The python standard library is not available

## Language features To be decided   **[TBD]**

* Scope & Implementation of Lists, Dictionaries, Sets, Tuples, Objects, Classes, import
* Tuple unpacking
* List access
* Blank lines are valid [2.1.8]
* Whitespace separates otherwise ambigious tokens [2.1.9]
* Identifiers follow the syntax [a-zA-Z_][a-zA-Z_0-9]* - the extended syntax for identifiers - for not Roman literals is not supported (yet)
* The following identifiers are reserved:
 * and as assert break class continue def del elif else except finally for from global if
 * import in is lambda nonlocal not or pass raise return try while with yield True False None 
* Reserved classes of identifiers are not supported as yet [2.3.2]
* There may be an additional syntax to assist with tweaking C compilation.
* This may use the term "pragma"
* How to handle/provide exceptions, if at all -- Seems odd not to

