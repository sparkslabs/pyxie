#!/usr/bin/python

blank_line = ""

source = []
def Print(*args):
    y = " ".join([str(x) for x in args])
    source.append(y)

class C_Program(object):
    def __init__(self):
        self.includes = []
        self.main_cframe = C_Frame()

    def generate(self):
        frame_lines = self.main_cframe.concrete()
        for include in self.includes:
            Print( "#include "+ include )

        Print()
        Print("using namespace std;")
        Print()
        Print("int main(int argc, char *argv[])")
        Print("{")
        for line in frame_lines:
            Print("    "+ line)
        Print("    "+ "return 0;")
        Print("}")

class C_Frame(object):
    def __init__(self):
        self.identifiers = []
        self.statements = []

    def concrete(self):
        block = []
        for identifier in self.identifiers:
            decl_code = identifier.decl_code()
            block.append(decl_code + ";")

        block.append(blank_line)
        for statement in self.statements:
            code = statement.code()
            block.append(code + ";")
        return block

class Identifier(object):
    def __init__(self, ctype, name):
        self.ctype = ctype
        self.name = name

    def decl_code(self):
        return self.ctype + " " + self.name

class Assigment(object):
    def __init__(self, lvalue, rvalue):
        self.lvalue = lvalue
        self.rvalue = rvalue

    def code(self):
        return self.lvalue + " = " + self.rvalue

class PrintStatement(object):
    def __init__(self, *args):
        self.args = args

    def code(self):
        return "cout << " + " << \" \" << ".join(self.args) + " << endl"

makefile_tmpl = """
all :
	g++ %(filename)s.c -o %(filename)s
"""


if __name__ == "__main__":

    # Build an example concrete syntax tree

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

    program.generate()

    import time
    import pprint
    import os

    pprint.pprint(source)
    now = int(time.time())
    dirname = str(now - 1427000000)
    print "BUILDING PROGRAM", dirname
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

