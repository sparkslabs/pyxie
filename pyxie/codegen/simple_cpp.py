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

blank_line = ""

source = []
def Print(*args):
    y = " ".join([str(x) for x in args])
    source.append(y)

def reset_parser():
    global source
    source = []

def mkStatement(statement_spec):
    ss = statement_spec
    if ss[0] == "assignment":
        return Assigment( ss[1], ss[3], ss[2])

    if ss[0] == "print_statement":
        return PrintStatement(*statement_spec[1:])


class C_Program(object):
    def __init__(self):
        self.includes = []
        self.main_cframe = C_Frame()
        self.name = ""

    @classmethod
    def fromjson(klass, json):
        program = klass()
        prog_desc = json["PROGRAM"]
        program.name = prog_desc["name"]
        program.includes = list(prog_desc["includes"])
        main_spec = prog_desc["main"]["c_frame"]
        for identifier in main_spec["identifiers"]:
            program.main_cframe.identifiers.append(Identifier(identifier[1], identifier[2]))

        for statement in main_spec["statements"]:
            conc_statement = mkStatement(statement)
            program.main_cframe.statements.append(conc_statement)


        return program

    def generate(self):
        frame_lines = self.main_cframe.concrete()
        seen = {}
        for include in self.includes:
            if not seen.get(include, False):
                # Only output each include once
                Print( "#include "+ include )
                seen[include] = True

        Print()
        Print("using namespace std;")
        Print()
        Print("int main(int argc, char *argv[])")
        Print("{")
        for line in frame_lines:
            Print("    "+ line)
        Print("    "+ "return 0;")
        Print("}")

    def json(self):
        return { "PROGRAM": {"name": self.name,
                             "includes" : self.includes,
                             "main": self.main_cframe.json()}
               }

class C_Frame(object):
    def __init__(self):
        self.identifiers = []
        self.statements = []

    def json(self):
        for y in self.statements:
            Print(y)
        return {"c_frame": {"identifiers" : [ x.json() for x in self.identifiers ],
                            "statements" : [y.json() for y in self.statements ] }
               }

    def concrete(self):
        block = []
        for identifier in self.identifiers:
            decl_code = identifier.decl_code()
            block.append(decl_code + ";")

        block.append(blank_line)
        for statement in self.statements:
            if statement:
                code = statement.code()
                block.append(code + ";")
        return block

class Identifier(object):
    def __init__(self, ctype, name):
        self.ctype = ctype
        self.name = name

    def json(self):
        return ["identifier", self.ctype, self.name ]

    def decl_code(self):
        return self.ctype + " " + self.name

class Assigment(object):
    def __init__(self, lvalue, rvalue, assigntype="="):
        self.lvalue = lvalue
        self.rvalue = rvalue
        self.assigntype = assigntype

    def json(self):
        return ["assignment", self.lvalue, self.assigntype, self.rvalue ]

    def code(self):
        return self.lvalue + " "+self.assigntype+" " + self.rvalue

def todo(*args):
    print("TODO", " ".join([repr(x) for x in args]))

class ArgumentList(object):
    def __init__(self, *args):
        self.args = args
    def json(self):
        return list(self.args[:])

    def code_op_F(self, arg):
        if arg[1] == "plus": return "+"
        if arg[1] == "minus": return "-"
        if arg[1] == "times": return "*"
        if arg[1] == "divide": return "/"
        return None

    def code_op(self,arg):
        c_op = self.code_op_F(arg)
        if c_op:

            arg1 = arg[2]
            arg2 = arg[3]
            # We would like to try to assert here that the values on both sides
            # are integers, but at present we cannot do that, since we use too simplistic
            # a structure. If I remove that constraint, we can generate more code.
            # But we will need to revisit this.
            lit_arg1 = self.code_arg(arg1)
            lit_arg2 = self.code_arg(arg2)

            result = "(" + lit_arg1 + c_op + lit_arg2 + ")"
            return result
        todo("Handle code ops for anything other than plus/int,int")
        raise NotImplementedError("Handle code ops for anything other than plus/int,int" + repr(arg))


    def code_arg(self, arg):
        if arg[0] == "identifier":
            return arg[1]
        if arg[0] == "integer":
            return repr(arg[1])
        if arg[0] == "string":
            carg = arg[1].replace('"', '\\"')
            return '"' + carg + '"' # Force double quotes
        if arg[0] == "double":
            return repr(arg[1])
        if arg[0] == "boolean":
            return arg[1]
        if arg[0] == "op":
            return self.code_op(arg)
        todo("Handle print value types that are more than the basic types")
        raise NotImplementedError("Handle print value types that are more than the basic types" + repr(arg))

    def code_list(self):
        cargs = []
        for arg in self.args:
            c_str = self.code_arg(arg)
            cargs.append(c_str)
        return cargs

    def code(self):
        return ",".join(self.code_list())

class PrintStatement(object):
    def __init__(self, *args):
        self.args = args
        self.arg_list = ArgumentList(*args)

    def json(self):
        return ["print_statement" ] + self.arg_list.json()

    def code(self):
        return "cout << " + " << \" \" << ".join(self.arg_list.code_list()) + " << endl"

makefile_tmpl = """
all :
	g++ %(filename)s.c -o %(filename)s
"""

def build_program(json):
    json = C_Program.fromjson(json)


if __name__ == "__main__":



    if 1:
        progj = {'PROGRAM': {'includes': ['<iostream>'],
                             'main': {'c_frame': {'identifiers': [],
                                                  'statements': [['print_statement',
                                                                  ['op',
                                                                   'plus',
                                                                   ['integer', 1],
                                                                   ['integer', 1]]]]}},
                             'name': 'hello_operators'}}

        program = C_Program.fromjson(progj)
        print program

        program.generate()
        import time
        import pprint
        import os

        pprint.pprint(source, width=200)
        now = int(time.time())
        dirname = str(now - 1427000000)
        # Print("BUILDING PROGRAM", dirname)
        os.mkdir(dirname)
        f = open(os.path.join(dirname,program.name+".c"), "w")
        for line in source:
            f.write(line)
            f.write("\n")
        f.close()

        makefile = makefile_tmpl % {"filename": program.name }
        f = open(os.path.join(dirname,"Makefile"), "w")
        f.write(makefile)
        f.close()

        os.chdir(dirname)
        os.system("make")



    # Build an example concrete syntax tree
    if 0:
        program = C_Program()

        program.name = ("hello")
        program.includes.append("<iostream>")
        program.includes.append("<string>")

        main = program.main_cframe
        main.identifiers.append(Identifier("string", "greeting"))
        main.identifiers.append(Identifier("string", "name"))
        main.statements.append(Assigment("greeting", '"hello"'))
        main.statements.append(Assigment("name", '"world"'))
        main.statements.append(PrintStatement("greeting", "name"))

        import pprint

        progj = program.json()

        pprint.pprint(progj)

        program_clone = C_Program.fromjson(progj)
        progj2 = program_clone.json()

        program = program_clone

        Print("--------------------------------------------------------------")
        pprint.pprint(progj2)

        program.generate()

        import time
        import pprint
        import os

        pprint.pprint(source, width=200)
        now = int(time.time())
        dirname = str(now - 1427000000)
        Print("BUILDING PROGRAM", dirname)
        os.mkdir(dirname)
        f = open(os.path.join(dirname,program.name+".c"), "w")
        for line in source:
            f.write(line)
            f.write("\n")
        f.close()

        makefile = makefile_tmpl % {"filename": program.name }
        f = open(os.path.join(dirname,"Makefile"), "w")
        f.write(makefile)
        f.close()

        os.chdir(dirname)
        os.system("make")

