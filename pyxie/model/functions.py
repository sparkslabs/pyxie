#!/usr/bin/python

"""
This file contains aspects related to modelling functions.

Python functions return values, these values can be:
* None
* Basic objects - int, float, string, boolean
* Complex objects - lists, dicts, instances from user classes
* Iterators/Generators

Functions can be:
* Built in
* User defined.

This file is primarily focussed on built in functions at the
moment, to facilitate "range"

TODO: This file needs a major rethink
"""

from __future__ import print_function
from __future__ import absolute_import

# built_ins = ("range", "print")

# Might be worth considering bunging all the builtins into seperate modules
# to be auto-discovered to populate this structure. It'd make creating custom
# versions easier potentially.

# This won't actually be used, it's here to help figure out what's needed
range_raw_code_template = """
    int count;
    range range_gen = range(5);
    while (true) {
        try {
            count = range_gen.next();
        } catch (StopIteration s) {
            break;
        }
        std::cout << count;
    }
"""


# This might well be used
icvdt = iterated_code_variable_declarations_template = """
    %(ITERATED_TYPE)s %(IDENTIFIER)s;
    %(ITERATOR_TYPE)s %(ITERATOR)s_gen_%(UNIQIFIER)s = %(ITERATOR)s;
"""

# This might well be used
icact = iterated_code_actual_code_template = """
    while (true) {
        try {
            %(IDENTIFIER)s = %(ITERATOR)s_gen_%(UNIQIFIER)s.next();
        } catch (StopIteration s) {
            break;
        }
        %(BODY)s # Itself uses %(IDENTIFIER)s
    }
"""

# This next line doesn't seem likely to be what we want here.
iterated_code_template = icvdt + icact
"""
    %(ITERATED_TYPE)s %(IDENTIFIER)s;
    %(ITERATOR)s %(ITERATOR)s_gen_%(UNIQIFIER)s = %(ITERATED_TYPE)s %(ITERATOR)s(5);
    while (true) {
        try {
            %(IDENTIFIER)s = %(ITERATOR)s_gen_%(UNIQIFIER)s.next();
        } catch (StopIteration s) {
            break;
        }
        %(BODY)s # Itself uses %(IDENTIFIER)s
    }
"""

in_the_above = {
        "ITERATED_TYPE" : "The type of the values created by this iterator",
        "IDENTIFIER" : "The identifier that takes the value created by the iterator for use in the loop body",
        "ITERATOR" : "The specific iterator that gets 'called' creating instances to iterate over",
        "UNIQIFIER" : "A unique id added to ensure that instances in the code as used are all new",
        "BODY" : "A set of 1 or more instructions that uses the values",
    }



builtins = {
             "range": {
                         "iterator": True,
                         "values_type": "integer",
                         "iterator_ctype" : "range",  # The name of the C function/struct/class
                         "code_template" : iterated_code_template, # Probably not what we want
                         "variable_declarations_template" :  icvdt,
                         "actual_code_template" :  icact,
                     }
            }

# Inside <Servo.h>
arduino_profile_function_calls = {
             "Servo": {
                         "iterator": False,
                         "return_ctype": "Servo", # C type of the returned value
                      }
    }

arduino_profile_types = {
             "Servo": {
                 }
    }


templates = { "iterator" : { "declarations" : icvdt,
                             "code" : icact,
                           }
            }
