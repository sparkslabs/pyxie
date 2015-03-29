#!/usr/bin/python

blank_line = ""

source = []
def Print(*args):
    y = " ".join([str(x) for x in args])
    source.append(y)

def mkStatement(statement_spec):
    ss = statement_spec
    if ss[0] == "assigment":
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
            print "IDENTIFIERS"
            program.main_cframe.identifiers.append(Identifier(identifier[1], identifier[2]))

        for statement in main_spec["statements"]:
            conc_statement = mkStatement(statement)
            program.main_cframe.statements.append(conc_statement)


        return program

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
            print y
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
        return ["assigment", self.lvalue, self.assigntype, self.rvalue ]

    def code(self):
        return self.lvalue + " "+self.assigntype+" " + self.rvalue

class PrintStatement(object):
    def __init__(self, *args):
        self.args = args

    def json(self):
        return ["print_statement" ] + list(self.args[:])

    def code(self):
        return "cout << " + " << \" \" << ".join(self.args) + " << endl"

makefile_tmpl = """
all :
	g++ %(filename)s.c -o %(filename)s
"""

def build_program(json):
    json = C_Program.fromjson(json)


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

    import pprint

    progj = program.json()

    pprint.pprint(progj)

    program_clone = C_Program.fromjson(progj)
    progj2 = program_clone.json()

    program = program_clone

    print "--------------------------------------------------------------"
    pprint.pprint(progj2)

    program.generate()

    import time
    import pprint
    import os

    pprint.pprint(source, width=200)
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

