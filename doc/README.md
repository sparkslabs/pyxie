Pyxie
=====

Pyxie will be a little python compiler.

Its initial target (which it does :) is to transform this python program:

    greeting = "hello"
    name = "world"

    print greeting, name

Into this C++ one:

    #include <iostream>
    #include <string>

    using namespace std;

    int main(int argc, char *argv[])
    {
        string greeting;
        string name;

        greeting = "hello";
        name = "world";
        cout << greeting << " " << name << endl;
        return 0;
    }

In practical terms, it means transforming this AST:

    ['program',
     ['statements',
      [['assignment_statement',
        ['greeting', 'IDENTIFIER', 1],
        ['ASSIGN', '='],
        ['value_literal', 'hello', 'STRING', 1]],
       ['assignment_statement',
        ['name', 'IDENTIFIER', 2],
        ['ASSIGN', '='],
        ['value_literal', 'world', 'STRING', 2]],
       ['print_statement ',
        [['value_literal', 'greeting', 'IDENTIFIER', 4],
         ['value_literal', 'name', 'IDENTIFIER', 4]]]]]]

Into this C program representation:

    {
        "PROGRAM": {
            "name": "hello",
            "includes": [ "<iostream>", "<string>" ],
            "main": {
                "c_frame": {
                    "identifiers": [
                        [ "identifier", "string", "greeting" ],
                        [ "identifier", "string", "name" ]
                    ],
                    "statements": [
                        [ "assignment", "greeting", "=", "\"hello\"" ],
                        [ "assignment", "name", "=", "\"world\"" ],
                        [ "print_statement", "greeting", "name" ]
                    ]
                }
            }
        }
    }

The process at present is as follows:

 - There is a python parser, which generates a JSON-able AST.
 - There is a code generator, that takes a JSON-able representation of a C++
   program and generates C++ code from that
 - There is a piece of code that transforms the JSON-AST into the C++ representation.


### Notes

It's worth noting that yes, expecting <string> and so on to exist on
a microcontroller is wishful thinking. As a first step though getting
something going is what matters here.






