
#
# Copyright 2018 Michael Sparks
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

# ========================================================================================
# Start of a "detangled" representation of C++ as form of AST
# classes these roughly the tangled representations' structure for now.
# ----------------------------------------------
#
# FIXME: This all needs work.
#


class _assignment_statement(object):  #NOTE: TBC
    def __init__(self, lvalue, rvalue, assign_operator):  # Assume assign_operator is "="
        self.lvalue = lvalue
        self.rvalue = rvalue   # rvalues seem to a mixture of types.
        self.assign_operator = assign_operator

        assert self.assign_operator.cpp() == "="

    def cpp(self):
        self.lvalue.cpp() + " " +  self.assign_operator.cpp() + " " + self.rvalue.cpp()

class _empty_statement(object):   #NOTE: TBC # NB, means "pass"
    def cpp(self):
        return ";"

class _break_statement(object):  #NOTE: TBC
    def cpp(self):
        return "break"

class _continue_statement(object):  #NOTE: TBC
    def cpp(self):
        return "continue"

class _function_call(object):  #NOTE: TBC
    def __init__(self, identifier_expression, *args):
        self.identifier_expression = identifier_expression
        self.args = args

    def cpp(self):
        call_label = self.identifier_expression.cpp()

        if call_label == "print":  # Handle special casing of "print" function call
            return _print_statement(args).cpp()

        arg_list = _argument_list(args).cpp()
        call_label = self.identifier.cpp()

        return call_label + "(" + arg_list + ")"


class _argument_list(object):  #NOTE: TBC
    def __init__(self, *args):
        self.args = args
    def cpp(self):
        return ",".join(  [ arg.cpp() for arg in self.args ]  )   


class _expression_statement(object):   #NOTE: TBC
    def __init__(self, expression):
        self.expression = expression
    def cpp(self):
        return self.expression.cpp()
 
class _print_statement(object):  #NOTE: TBC
    def __init__(self, list_args):  # list_args : list of cpp args - that is things that have a .cpp() method
        self.list_args = list_args
    def cpp(self):
        list_cpp_args = [ arg.cpp() for arg in self.list_args ]
        list_cpp_args = " << \" \" << ".join( list_cpp_args )
        return "( std::cout << " +  list_cpp_args +  " << std::endl )"

class _iterable(object):  #NOTE: TBD
    # FIXME: Used _for_iter_loop_statement
    # FIXME: REPRESENTS AN ITERABLE *EXPRESSION*
    # FIXME: method:: iterable.cpp_type()
    # FIXME: method:: iterable.cpp()
    # FIXME: method:: iterable.name()
    pass




#class _statements(object):
#    # FIXME: Used _for_iter_loop_statement
#    # FIXME: REPRESENTS A BLOCK OF STATEMENTS (sans enclosing braces - probably)
#    # * Implies that this also may have local variables.
#    # * Local variables will also have types/etc
#    # * *Python* local variables in here need to be migrated out to containing scope for definition.
#    #       - Not the case for C++ variables after all.
#    pass


class _for_iter_loop_statement(object):  #NOTE: TBC
    """
    Represents the C++ version of:
        for identifier in iterable:
            statements

    Since this does represents the C++ form it does not perform a transformation.
    Therefore everything it needs to know MUST be provided to it up front.
    """
    def __init__(self, identifier,
                       iterable,
                       statements):

        self.identifier = identifier
        self.iterable = iterable
        self.statements = statements

    def cpp(self):
        template = """
            %(ITERATOR_NAME)s = %(ITERATOR_EXPRESSION)s;
            while (true) {
                %(IDENTIFIER)s = %(ITERATOR_NAME)s.next();
                if (%(ITERATOR_NAME)s.completed())
                    break;

                %(BODY)s // Itself uses %(IDENTIFIER)s
            }
        """
        template_args =  { "ITERATOR_TYPE": self.iterable.cpp_type(),
                           "ITERATOR_EXPRESSION": self.iterable.cpp(),
                           "ITERATOR_NAME": self.iterable.name(),
                           "IDENTIFIER": self.identifier.cpp(),
                           "BODY": self.statements.cpp()
                         }


class _while_statement(object):  #NOTE: TBC
    def __init__(self, condition, statements):
        self.condition = condition
        self.statements = statements
    def cpp(self):
        cpp_condition = self.condition.cpp()
        cpp_statements = self.statements.cpp()
        code = "while ( %s ) { %s } " % (cpp_condition, cpp_statements )
        return  code


class _if_statement(object):  #NOTE: TBC
    def __init__(self, condition, block, extended_clause=None):
        self.condition = condition
        self.block = block
        self.extended_clause = extended_clause

    def cpp(self):
        cpp_condition = self.condition.cpp()
        cpp_block = self.block.cpp()
        code = "if ( %s ) { %s } " % (cpp_condition, cpp_block )
        if self.extended_clause:
            cpp_extended_clause = self.extended_clause.cpp()
            code = code = cpp_extended_clause
        return  code


class _else_if_clause(object):  #NOTE: TBC
    def __init__(self, condition, block, extended_clause=None):
        self.condition = condition
        self.block = block
        self.extended_clause = extended_clause

    def cpp(self):
        cpp_condition = self.condition.cpp()
        cpp_block = self.block.cpp()
        code = "else if ( %s ) { %s } " % (cpp_condition, cpp_block )
        if self.extended_clause:
            cpp_extended_clause = self.extended_clause.cpp()
            code = code = cpp_extended_clause
        return  code


class _else_clause(object):  #NOTE: TBC
    def __init__(self, block):
        self.block = block
    def cpp(self):
        cpp_block = self.block.cpp()
        return  "else { %s } " % (cpp_block, )


class  _identifier(object):  #NOTE: TBC
    # NOTE: ALSO USED in _for_iter_loop_statement
    # FIXME: CHECK COMPATIBILITY
    # FIXME: REPRESENTS AN IDENTIFIER (more specific than an LVALUE)
    # FIXME: method:: iterable.cpp()

    def __init__(self, name, ctype=None):
        self.ctype = ctype
        self.name = name

    def cpp_decl(self):   # FIXME: Really? Maybe, yes.
        if ctype == None:
            raise ValueError("This label does not have a type")
        return self.ctype + " " + self.name

    def cpp(self):
        return self.name


class _statements_block(object):  #USED
    # TODO: SHOULD THIS ACTUALLY INCLUDE THE BRACES?
    def __init__(self, identifiers, statements):
        self.identifiers = identifiers
        self.statements = statements

    def cpp(self):
        decl_lines = [ i.cpp_decl() + ";" for i in self.identifiers ]
        if len(decl_lines) > 0:
            decl_lines.append("")
        statement_lines = [ s.cpp() + ";" for s in self.statements ]
        return "\n".join( decl_lines + statement_lines )


class _core_include(object):  # USED
    def __init__(self, include_name):
        self.include_name = include_name
    def cpp(self):
        return  "#include <%s>" % (self.include_name, )


class _relative_include(object):  # USED
    def __init__(self, include_name):
        self.include_name = include_name
    def cpp(self):
        return  '#include "%s"' % (self.include_name, )


class _using_namespace(object):  # USED
    def __init__(self, namespace):
        self.namespace = namespace
    def cpp(self):
        return  "using namespace %s" % (self.namespace, )


class _function_decl(object):  # USED
    def __init__(self, return_type, name, argument_decls, statements):
        self.return_type = return_type
        self.name = name
        self.argument_decls = argument_decls
        self.statements = statements
    def cpp(self):
        return  "%(return_type)s %(name)s(%(argument_decls)s) {\n%(statements)s\n}" % {
                "return_type" : self.return_type.cpp(),
                "name" : self.name.cpp(),
                "argument_decls" : self.argument_decls.cpp(), # Identifier list?
                "statements" : self.statements.cpp()
            }


class  _label(object):  # USED
    def __init__(self, label):
        self.label = label

    def cpp(self):
        return self.label


class _simple_typespec(object):  # USED
    def __init__(self, type_label):
        self.type_label = type_label
    def cpp(self):
        return self.type_label.cpp()

    def cpp_decl(self, thing):
        return self.type_label.cpp() + " " + thing.cpp()


class _emb_typespec(object):   # USED
    def __init__(self, type_label):
        self.type_label = type_label

    def cpp_decl(self, thing):
        return self.type_label.cpp() % { "TYPED_THING" : thing.cpp() }


class _argument_decls(object):   # USED
    def __init__(self, *arg_specs):
        self.arg_specs = arg_specs
    def cpp(self):
        cpp_args = []
        for arg_spec in self.arg_specs:
            type_spec, label = arg_spec
            arg_decl = type_spec.cpp_decl(label)
            cpp_args.append(arg_decl)
        cpp_arg_spec = ", ".join(cpp_args)
        return cpp_arg_spec


class _string_literal(object): # USED
    def __init__(self,  raw_string):
        self.raw_string = raw_string
    def cpp(self):
        r = '"' +self.raw_string.replace('"', '\\"') + '"'
        return r


class _int_literal(object):  # USED
    def __init__(self,  raw_int):
        self.raw_int = raw_int
    def cpp(self):
        return repr(self.raw_int)


class _return_statement(object): # USED
    def __init__(self,  return_value):
        self.return_value= return_value
    def cpp(self):
        return "return (%s)" % (self.return_value.cpp(), )


# NOTE: WOULD BE NICE TO ACTUALLY CHAIN THINGS, BUT NOT FOR NOW
class _op(object): # USED
    def __init__(self, op_literal, left, right):
        self.op_literal = op_literal
        self.left = left
        self.right = right

    def cpp(self):
        left = self.left.cpp()
        right = self.right.cpp()

        if type(self.right) == _op:
            right = "(" + right + ")"

        if type(self.left) == _op:
            left = "(" + left + ")"

        return left + " " + self.op_literal + " " + right


def mkMainFunction(identifiers, statements): # USED
    lstatements = statements[:]
    lstatements.append(_return_statement(_int_literal(0)))
    mainFunction  = _function_decl(int_type,       # return_type,
                                _label("main"),  # name,
                                _argument_decls(
                                            (int_type, _label("argc")),
                                            (array_char_pointer_type, _label("argv"))
                                ),
                                _statements_block(
                                                    identifiers, # Identifiers in the main code
                                                    lstatements
                                                    )
                                )
    return mainFunction


void_type = _simple_typespec(_label("void")) # USED
int_type =  _simple_typespec(_label("int"))  # USED
array_char_pointer_type =  _emb_typespec(_label("char *%(TYPED_THING)s[]"))  # USED

class _program(object):  # USED
    def __init__(self, includes, decls, functions):
        self.includes = includes
        self.decls = decls
        self.functions = functions
    def cpp(self):
        r = []
        for i in includes:
            r.append(i.cpp())
        for decl in self.decls:
            r.append("")
            r.append(decl.cpp()+";" )
        for function in functions:
            r.append("")
            r.append(function.cpp() )

        return "\n".join(r)

if __name__ == "__main__":

    includes = [
        _core_include("iostream"),
        _relative_include("iterators.cpp")
        ]
    decls = [
        _using_namespace("std")
        ]


    debugFunction = _function_decl(void_type,               # return_type
                                   _label("DebugFunction"), # name
                                   _argument_decls(),
                                   _statements_block(
                                       [], # identifier decls
                                       [  # statements
                                           _op( "<<",
                                                _op( "<<",
                                                    _label("std::cout"),
                                                    _string_literal('DEBUG "FUNCTION" CALLED'),
                                                ),
                                                _label("std::endl"),
                                            )
                                       ])
                                   )

    # This is what the generated code gets inserted to -- at present
    mainFunction = mkMainFunction([ # List of identifiers
                                  ],
                                  [  # List of statements
                                  ])

    functions = [ debugFunction, mainFunction ]

    p = _program( includes, decls, functions )
    print(p.cpp())
