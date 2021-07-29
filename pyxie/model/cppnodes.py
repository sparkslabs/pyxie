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

from pyxie.model.iinodes import iiIdentifier

from pyxie.transform.profiles import cpp_templates
from pyxie.model.functions import builtins

import pprint

unique_id = 0 # FIXME: Naming - Used to generate unique ids within for statements. 
              # FIXME: Implies there should be a better way of doing this.
              # FIXME: WORSE: this isn't even actually used - since it happens in the wrong place.

from pyxie.util import todo
from pyxie.util import get_blank_line
from pyxie.util import Print

# CppNodes representing C++ Programs. From these you can generate C++ code.

# Below here should be C++ Nodes, representing C++ programs
# They should be able to generate C++ code directly from the data they have.
# They should NOT be doing any transformations.
# The fact they do at present should be viewed as a areas needing improvements


class CppNode(object):
    pass

class CppProgram(CppNode):
    def __init__(self):
        self.includes = []
        self.main_cframe = CppFrame()
        self.name = ""


    def code(self, profile = "default"):
        print("BUILDING FOR PROFILE", profile)
        frame_raw = self.main_cframe.code()
        frame_lines = frame_raw.split("\n")

        seen = {}
        for include in self.includes:
            if not seen.get(include, False):
                # Only output each include once
                Print( "#include "+ include )
                seen[include] = True

        print_def = cpp_templates.get(profile, cpp_templates.get("default"))
        frame_text = "\n".join(["   "+line for line in frame_lines])

        Print(print_def % { "FRAME_TEXT": frame_text } )

    def json(self):
        return { "PROGRAM": {"name": self.name,
                             "includes" : self.includes,
                             "main": self.main_cframe.json()}
               }

class CppFrame(CppNode):
    def __init__(self):
        self.identifiers = []
        self.statements = []

    def json(self):
        for y in self.statements:
            Print(y)
        return {"c_frame": {"identifiers" : [ x.json() for x in self.identifiers ],
                            "statements" : [y.json() for y in self.statements ] }
               }

    def code(self):
        block = []
        for identifier in self.identifiers:
            decl_code = identifier.decl_code()
            block.append(decl_code + ";")

        block.append(get_blank_line() )
        for statement in self.statements:
            if statement:
                code = statement.code()
                if code is None:
                    print("STATEMENT IS None, WHY?", statement)
                block.append(code + ";")
        block_as_string = "\n".join(block)
        return block_as_string

class CppIdentifier(CppNode):
    def __init__(self, ctype, name):
        self.ctype = ctype
        self.name = name

    def json(self):
        return ["identifier", self.ctype, self.name ]

    def decl_code(self):
        return self.ctype + " " + self.name

class CppAssignment(CppNode):
    def __init__(self, lvalue, rvalue, assigntype="="):
        self.lvalue = lvalue
        self.rvalue = rvalue   # rvalues seem to a mixture of types.
        self.assigntype = assigntype
        print("CppAssignment.__init__   LVALUE", lvalue, type(lvalue), repr(lvalue))
        print("CppAssignment.__init__   RVALUE", rvalue, type(rvalue), repr(rvalue))

    def json(self):
        return ["assignment", self.lvalue, self.assigntype, self.rvalue ]

    def code(self):
        try:
            rvalue_tag = self.rvalue.tag
        except AttributeError: # FIXME: This is borken
            rvalue_tag = None

        if rvalue_tag == "function_call":
            print("Aha!",self.rvalue)
            crvalue = CppArgumentList(self.rvalue)
            crvalue = crvalue.code()
            print("AHA!", crvalue)

        elif rvalue_tag == "op":
            crvalue = CppArgumentList(self.rvalue)
            crvalue = crvalue.code()
        else:
            print("Are we here?")
            crvalue = self.rvalue
            print("Are we here?",crvalue)

        print("self.lvalue",self.lvalue)
        print("self.assigntype",self.assigntype)
        print("crvalue",type(crvalue), crvalue)
        return self.lvalue + " "+self.assigntype+" " + crvalue

class CppEmptyStatement(CppNode):
    # A pass statement is not a commented out statement.
    #
    # By that this:
    # while True: pass
    #
    # Is equivalent to while(true);
    # As opposed to while(true)
    #
    # So that's why this returns ";" not ""
    def json(self):
        return ["pass_statement"]

    def code(self):
        return ";"

class CppBreakStatement(CppNode):
    def json(self):
        return ["break_statement"]

    def code(self):
        return "break"

class CppContinueStatement(CppNode):
    def json(self):
        return ["continue_statement"]

    def code(self):
        return "continue"

class CppFunctionCall(CppNode):
    def __init__(self, identifier, args):
        self.args = args
        self.identifier = identifier
        self.arg_list = CppArgumentList(*args)

    def json(self):
        return ["function_call", self.identifier ] + self.arg_list.json()

    def code(self):
        if self.identifier.tag == "attributeaccess":
            expression = self.identifier.expression
            attribute = self.identifier.attribute

            c_expression = "(" + expression.identifier + ")"
            c_attribute = attribute.identifier

            identifier = c_expression + "." + c_attribute

        else:
            identifier = self.identifier.identifier

            # FUDGE: The following would need to be profile specific
            #
            # It probably also needs reviewing/revising later on
            if identifier == "print":
                X = CppPrintStatement(*self.args)
                return X.code()

        arglist = ", ".join(self.arg_list.code_list())
        return identifier + "(" + arglist + ")"

class CppArgumentList(CppNode):
    def __init__(self, *args):
        self.args = args

    def json(self):
        return list(self.args[:])

    def code_list(self):                                  # PERFORMING A TRANSFORM FROM AN IINODE
        cargs = [ code_arg(arg) for arg in self.args ]    # METHOD IS USED OUTSIDE THIS CLASS
        return cargs

    def code(self):                                                   # TRANSFORM INVOLVES IINODES :-(
        return ",".join(  [ code_arg(arg) for arg in self.args ]  )   # TRANSFORM INVOLVES IINODES :-(

class CppExpressionStatement(CppNode):
    def __init__(self, expression):
        self.expression = expression

    def json(self):
        return ["expression_statement", self.expression ]

    def code(self):
        print(self.expression)
        if self.expression.tag == "function_call":
            cvalue = CppArgumentList(self.expression)
            cvalue = cvalue.code()
        else:
            raise Exception("Fail to understand how to generate code for %s" % repr(self.expression) )

        return cvalue

class CppPrintStatement(CppNode):
    def __init__(self, args):
        self.args = args
        self.arg_list = CppArgumentList(*args)

    def json(self):
        return ["print_statement" ] + self.arg_list.json()

    def code(self):
        return "( std::cout << " + " << \" \" << ".join(self.arg_list.code_list()) + " << std::endl )"

class CppForStatement(CppNode):
    def __init__(self, identifier, iterable, statements, for_statement_pynode):
        self.raw_identifier = identifier
        self.raw_iterable = iterable
        self.raw_statements = list(statements)
        self.block_cframe = CppFrame()
        self.for_statement_pynode = for_statement_pynode  

        # FIXME: for_statement_pynode
        # This is pulled in, in this slightly bizarre way due to the way variables are found during
        # the process of analysis. Variables are found at the python stage, and these effectively
        # get used to generate declarations.
        #
        # The problem here is that the expression being iterated over needs a name so that it can be
        # treated as an iterator. As a result, it cannot be given a name at this stage.
        # As a result the whole pynode gets pulled over.
        #
        # This is clearly a bug, but it's really symptomatic of how and where analysis is performed.
        # For now it means anything to do with unique ids *here* is irrelevant.
        #

        for statement in self.raw_statements:
            conc_statement = mkStatement(statement)
            self.block_cframe.statements.append(conc_statement)

    def json(self):
        return ["for_statement", self.raw_condition, self.raw_iterable, self.raw_statements ]

    def code(self):
        #
        # The following is the sort of code we want to generate inline.
        # This actually implements what we're after.
        # However it requires some declarations to be in place really of the the find variables kind
        # That said, C++ allows inline delcarations like this (for good or ill), so maybe just do
        # this in the first instance, and leave improvements for refactoring???
        #
        # Actually this discussion is useful, but it turns out to allow nested generator usage
        # ie for x in range(5): for y in range(x): print x,y
        # It requires this to be done closer to what could be viewed as "properly"
        #
#            %(ITERATOR_TYPE)s %(ITERATOR_NAME)s = %(ITERATOR_EXPRESSION)s;
        template = """
            %(ITERATOR_NAME)s = %(ITERATOR_EXPRESSION)s;
            while (true) {
                %(IDENTIFIER)s = %(ITERATOR_NAME)s.next();
                if (%(ITERATOR_NAME)s.completed())
                    break;

                %(BODY)s // Itself uses %(IDENTIFIER)s
            }
        """
        global unique_id
        unique_id = unique_id+1

        iterator_ctype = "range"
        iterator_expression = self.raw_iterable ## NOTE THIS RESULTS IN ['iterate_over', ['function_call', ['identifier', 'range'], [['integer', 5]]]]- so that needs work

        print("OK, USE THIS THEN", self.for_statement_pynode.expression.ivalue_name)
        iterator_name = self.for_statement_pynode.expression.ivalue_name

        if self.raw_iterable.tag == "iterator":
            iterable = self.raw_iterable.expression

            if iterable.tag == "function_call":
                print("FUNCTION_CALL", iterable.iifunc_object)
                assert type(iterable.iifunc_object) == iiIdentifier

                identifier = iterable.iifunc_object.identifier
                if identifier in builtins:
                    print("YAY")
                    pprint.pprint( builtins[identifier] )
                    iterator_ctype = builtins[identifier]["iterator_ctype"]
                    print("iterator_name -- ", iterator_ctype)
                    print("YAY")

                print(iterable)
                fcall = CppFunctionCall(iterable.iifunc_object,iterable.iifunc_call_args)
                fcall_code = fcall.code()
                iterator_expression = fcall_code

        template_args =  { "ITERATOR_TYPE": iterator_ctype,
                           "ITERATOR_EXPRESSION": iterator_expression,
                           "ITERATOR_NAME": iterator_name,
                           "IDENTIFIER": self.raw_identifier,
                           "BODY": self.block_cframe.code(),
                           "DEBUG": repr(dir(self.for_statement_pynode.expression))
                         }
        print("=== template args =================================================")
        pprint.pprint (template_args )
        print("--- template args -------------------------------------------------")
        if self.for_statement_pynode.expression.isiterator:
            identifier = self.for_statement_pynode.identifier
            print(identifier.get_type())
        print("=== end extractable template args =================================")
        print(template % template_args)

        print("----------------------------------------------------------")
        print(dir(self.for_statement_pynode))
        print(repr(self.for_statement_pynode))
        print("----------------------------------------------------------")
#        raise NotImplementedError("Haven't finished implementing CppForStatement yet...")
        code = template % template_args

        print("CODE", code)

        return code


class CppWhileStatement(CppNode): 
    # PURE EXISTS _while_statement

    def __init__(self, condition, *statements):
        self.raw_condition = condition
        self.raw_statements = list(statements)
        self.block_cframe = CppFrame()

        for statement in self.raw_statements:
            conc_statement = mkStatement(statement)
            self.block_cframe.statements.append(conc_statement)

    def json(self):
        return ["while_statement", self.raw_condition] + self.raw_statements

    def code(self):

        cpp_condition = CppArgumentList(self.raw_condition).code()
        cpp_block_code = self.block_cframe.code()

        code = "while ( %s) { %s }" % (cpp_condition, cpp_block_code)

        return code

class CppIfStatement(CppNode):
    # PURE EXISTS _if_statement

    def __init__(self, condition, statements, extended_clause=None):
        self.raw_condition = condition
        self.raw_statements = list(statements)
        self.extended_clause = extended_clause

        self.block_cframe = CppFrame()
        for statement in self.raw_statements:
            conc_statement = mkStatement(statement)
            self.block_cframe.statements.append(conc_statement)

    def json(self):
        result = ["if_statement", self.raw_condition, self.raw_statements ]
        if self.extended_clause is not None:
            result.append(extended_clauses.json())

    def code(self):
        extended_clauses_code = None
        condition_code = CppArgumentList(self.raw_condition).code()
        block_code = self.block_cframe.code()
        if self.extended_clause:
            if self.extended_clause.tag == "elif_clause":
                condition = self.extended_clause.condition
                statements =  self.extended_clause.statements
                if self.extended_clause.extended_clause:
                    extended_sub_clause =  self.extended_clause.extended_clause
                    extended_clauses_code = CppElseIfClause( condition, statements, extended_sub_clause ).code()
                else:
                    extended_clauses_code = CppElseIfClause( condition, statements ).code()

            if self.extended_clause.tag == "else_clause":
                print("***************************************************")
                statements =  self.extended_clause.statements
                extended_clauses_code = CppElseClause( statements ).code()

        code = "if ( %s ) { %s } " % (condition_code, block_code )
        if extended_clauses_code:
            code = code + extended_clauses_code
        return code

class CppElseIfClause(CppNode):
    # PURE EXISTS _else_if_clause

    def __init__(self, condition, statements, extended_clause=None):
        self.raw_condition = condition
        self.raw_statements = list(statements)
        self.extended_clause = extended_clause

        self.block_cframe = CppFrame()
        for statement in self.raw_statements:
            conc_statement = mkStatement(statement)
            self.block_cframe.statements.append(conc_statement)

    def json(self):
        result = ["elif_clause", self.raw_condition, self.raw_statements ]
        if self.extended_clause is not None:
            result.append(extended_clause.json())

    def code(self):
        extended_clauses_code = None
        condition_code = CppArgumentList(self.raw_condition).code()
        block_code = self.block_cframe.code()
        if self.extended_clause:
            if self.extended_clause.tag == "elif_clause":
                print("***************************************************")
                condition = self.extended_clause.condition
                statements =  self.extended_clause.statements

                if self.extended_clause.extended_clause:
                    extended_sub_clause =  self.extended_clause.extended_clause
                    extended_clauses_code = CppElseIfClause( condition, statements, extended_sub_clause ).code()
                else:
                    extended_clauses_code = CppElseIfClause( condition, statements ).code()


            if self.extended_clause.tag == "else_clause":
                print("***************************************************")
                statements =  self.extended_clause.statements
                extended_clauses_code = CppElseClause( statements ).code()

        code = "else if ( %s ) { %s } " % (condition_code, block_code )
        if extended_clauses_code:
            code = code + extended_clauses_code
        return code

class CppElseClause(CppNode):
    # PURE EXISTS: _else_clause

    def __init__(self, statements):
        self.raw_statements = list(statements)

        self.block_cframe = CppFrame()
        for statement in self.raw_statements:
            conc_statement = mkStatement(statement)
            self.block_cframe.statements.append(conc_statement)

    def json(self):
        result = ["elif_clause", self.raw_statements ]

    def code(self):
        extended_clauses_code = None
        block_code = self.block_cframe.code()

        code = "else { %s } " % (block_code, )

        return code
