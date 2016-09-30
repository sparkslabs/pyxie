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

import os
import pprint
import time

import pyxie.codegen.profiles as profiles
import pyxie.codegen.simple_cpp

from pyxie.parsing.lexer import build_lexer
from pyxie.parsing.grammar import parse

from pyxie.model.pynode import jdump
from pyxie.model.transform import ast_to_cst

from pyxie.codegen.clib import files as clib_files
from pyxie.codegen.simple_cpp import C_Program, source, reset_parser

testdir = "test-data"
testprogs_dir = os.path.join(testdir, "progs")


def copy_file(source, dest):
    f = open(source, "rb")
    g = open(dest, "wb")
    g.write(f.read())
    f.close()
    g.close()

def remove_directory(build_dir):
    for filename in os.listdir(build_dir):
        try:
            os.unlink(os.path.join(build_dir, filename))
        except OSError as e :
            if e.errno == 21:
                remove_directory(os.path.join(build_dir, filename))
    os.rmdir(build_dir)


def get_test_programs(program_suffix):
    testprogs = [x for x in os.listdir(testprogs_dir) ]
    testprogs = [x for x in testprogs if x.endswith(program_suffix) ]
    return testprogs


def get_build_environment(filename, result_filename):
    rootdir = os.getcwd()

    lastslash_pos = filename.rfind("/")
    if lastslash_pos != -1:
        base_dir = filename[:lastslash_pos]
        base_filename = filename[lastslash_pos+1:]
    else:
        base_dir = "." # just a filename
        base_filename = filename

    cname = base_filename[:base_filename.rfind(".")]

    if not result_filename:
        result_filename = os.path.join(base_dir, cname)

    return {
            "rootdir" :rootdir,
            "base_dir" : base_dir,
            "base_filename":base_filename,
            "cname" : cname,
            "result_filename" : result_filename,
           }


def parse_file(somefile):
    lexer = build_lexer()
    reset_parser()
    data = open(somefile).read() + "\n#\n"
    AST = parse(data, lexer)
    AST.includes = lexer.includes
    print()
    print("parse_file: AST includes", AST.includes)
    print()
    print("parse_file: Raw Parsed AST ----------------------------------")
    print(AST)
    print("----------------------------------")
    print()
    return AST


def analyse_file(filename):
    try:
        AST = parse_file(filename)
        print("analyse_file: parse_file success------------")
    except:
        print("***** FAILED TO PARSE FILE *****")
        from pyxie.parsing.context import Context
        for cid in Context.contexts:
            context = Context.contexts[cid]
            print("CONTEXT",context.names)
        raise


    print("analyse_file: parse_file - AST json form follows ------------")
    pprint.pprint(AST.__json__())
    print("------------")
    print("")

    try:
        AST.analyse()
        print("analyse_file: Analysis success------------")
    except:
        print("***** FAILED TO ANALYSE FILE *****")
        from pyxie.parsing.context import Context
        for cid in Context.contexts:
            context = Context.contexts[cid]
            print("CONTEXT",context.names)
        raise

    print("analyse_file: Analysis results follow ------------")
    pprint.pprint(AST.__info__())
    print("------------")

def generate_code(cname, AST, profile, debug=False):
    CST = ast_to_cst(cname, AST)
    if debug:
        print("generate_code: CONCRETE C SYNTAX TREE: - - - - - - - - - - - - - - - - - - - -")
        print(pprint.pformat(CST))
        print("- - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -")
    program = C_Program.fromjson(CST)
    program.generate(profile)
    return pyxie.codegen.simple_cpp.source[:]


def codegen_phase(filename, result_filename, profile):
    build_env = get_build_environment(filename, result_filename)

    cname = build_env["cname"]

    AST = parse_file(filename)
    AST.analyse()
    print("codegen_phase: _______________________________________________________________")
    print("codegen_phase: GENERATING CODE")
    print()
    c_code = generate_code(cname, AST, profile, debug=True)  # Need the C NAME TO DO THIS
    print("codegen_phase: _______________________________________________________________")
    print("codegen_phase: Generated Program")
    print("\n".join(c_code))
    print("_______________________________________________________________")
    return c_code


def build_program(source, work_dir, name, profile):
    print("build_program: _______________________________________________________________")
    print("build_program: BUILDING", work_dir)
    print()
    print("build_program: Program to build:")
    pprint.pprint(source, width=200)
    print()

    extension = profiles.mainfile_extensions.get(profile,"c")

    source_filename = os.path.join(work_dir,name+"." +extension)

#    f = open(os.path.join(work_dir,name+"." +extension), "w")
    f = open(source_filename, "w")
    for line in source:
        f.write(line)
        f.write("\n")
    f.close()

    if os.path.exists("/usr/bin/indent"):
        try:
            print("build_program: TIDYING")
            print("build_program: /usr/bin/indent %s" % source_filename)
            os.system("/usr/bin/indent -npcs -brf -br -npsl -l120 -i4 -nut %s" % source_filename)
        except Exception as e:
            print("build_program: TIDYING Failed - continuing anyway")
            print("build_program: TIDYING error: %s %s" % (str(e), repr(e)))

    try:
        makefile_tmpl = profiles.makefile_templates[profile]
    except KeyError:
        makefile_tmpl = profiles.makefile_templates["default"]

    makefile = makefile_tmpl % {"filename": name }

    # This is hideously inefficient. It's simple though
    if os.path.exists(os.path.join(work_dir,"Makefile.in")):
        # MAKEFILE.IN EXISTS
        # Parse it into a dictionary
        f = open(os.path.join(work_dir,"Makefile.in"))
        lines = f.readlines()
        f.close()
        r = {}
        for line in lines:
            p = line.find("=")
            key, value = line[:p].strip(), line[p+1:].strip()
            r[key] = value

        # Loop through default makefile and replace values in it with overrides
        makefile_ = []
        makefile = makefile.split("\n")
        for line in makefile:
            if "=" in line:
                p = line.find("=")
                key, value = line[:p].strip(), line[p+1:].strip()
                if key in r:
                    makefile_.append( key + " = " + r[key])
                else:
                    makefile_.append(line)
            else:
                    makefile_.append(line)

        makefile = "\n".join(makefile_)

    f = open(os.path.join(work_dir,"Makefile"), "w")
    f.write(makefile)
    f.close()

    exclusions = profiles.clib_exclusions.get(profile, [])
    for filename in clib_files:
        if filename.endswith("_test.cpp"):
            # Skip main programs to avoid confusing profiles
            continue
        if filename in exclusions:
            print("build_program: Skipping", filename, "for profile", profile)
            continue

        f = open( os.path.join(work_dir,filename), "w")
        f.write(clib_files[filename])
        f.close()

    os.chdir(work_dir)
    os.system("make")
    print()
    print("build_program: Done!")
    print()


# Next function is called by compile_file, but could be called independently
# This is why both do "build_env", rather that expect the caller to
def compile_file(filename, profile, result_filename=None):

    build_env = get_build_environment(filename, result_filename)

    rootdir = build_env["rootdir"]
    base_dir = build_env["base_dir"]
    base_filename = build_env["base_filename"]
    cname = build_env["cname"]
    result_filename = build_env["result_filename"]

    c_code  = codegen_phase(filename, result_filename, profile)

    print("compile_file: COMPILING", filename)
    print("compile_file: IN", base_dir)
    print("compile_file: SOURCEFILE", base_filename)
    print("compile_file: cname", cname)
    print("compile_file: result_filename", result_filename)

    build_dir = os.path.join(base_dir, "build-"+str(int(time.time())))
    try:
        os.mkdir(build_dir)
    except OSError as e:
       if e.errno != 17: # Directory exists
           raise

    if (os.path.exists(result_filename+".Makefile.in")):
        # USER OPTIONS FOR COMPILING DETECTED - copy into build directory
        copy_file(result_filename+".Makefile.in", os.path.join(build_dir, "Makefile.in"))

    build_program(c_code, build_dir, cname, profile)

    os.chdir(rootdir)

    actual_result_file = (profiles.result_file[profile])(build_dir, cname)

    result_filename = (profiles.modify_result_file[profile])(result_filename)

    print("compile_file: BUILD DIR", build_dir)
    print("compile_file: RESULT FILE", actual_result_file)
    print("compile_file: DEST FILE", result_filename)
    print("compile_file: CWD", os.getcwd())

    os.rename(actual_result_file,result_filename)
    clean = False
    if clean:
        remove_directory(build_dir)
        if base_dir == ".":
            os.unlink("parsetab.py")
            os.unlink("parser.out")
    return


def parse_testfile(testprogs_dir, testfile, debug=False):
    print("parse_testfile: _______________________________________________________________")
    print("parse_testfile: PARSING", os.path.join(testprogs_dir,testfile))
    print()
    AST = parse_file(os.path.join(testprogs_dir,testfile))
    if debug:
        pprint.pprint(AST)
        JAST = jdump(AST)
        pprint.pprint(JAST)
    return AST


def compile_testfile(testprogs_dir, testfile, profile):
    # The compiled c name is the filename with the suffix removed
    p = testfile.rfind(".")
    cname = testfile[:p]

    AST = parse_testfile(testprogs_dir, testfile, debug=True)

    print("compile_testfile: _______________________________________________________________")
    print("compile_testfile: ANALYSING", os.path.join(testprogs_dir,testfile))
    print()
    AST.analyse()

    print("compile_testfile: _______________________________________________________________")
    print("compile_testfile: COMPILING", os.path.join(testprogs_dir,testfile))
    print()

    c_code = generate_code(cname, AST, profile, debug=True)

    # Create Work directory
    allresults_dir = os.path.join(testdir, "genprogs")
    thisresult_dir = os.path.join(allresults_dir, testfile)

    try:
        os.mkdir(allresults_dir)
    except OSError as e:
        pass # Can raise an exception if the directory exists, which is fine

    try:
        os.mkdir(thisresult_dir)
    except OSError as e:
       if e.errno != 17: # Directory exists
           raise

    build_program(c_code, thisresult_dir, cname, profile)


def parsing_tests():
    # Run parsing tests. These are in the "progs" test directory, and are in
    # filenames ending ".p"

    rootdir = os.getcwd()
    testprogs = get_test_programs(".p")

    for testfile in testprogs:
        AST = parse_testfile(testprogs_dir, testfile)
        pprint.pprint(AST)

        JAST = jdump(AST)
        pprint.pprint(JAST)

        os.chdir(rootdir)


def compilation_tests(profile):
    # ast_to_cst
    # Compilation Tests
    rootdir = os.getcwd()
    testprogs = get_test_programs(".pyxie")
    print("compilation_tests: TEST PROGS", testprogs)

    for testfile in testprogs:
        build_fail = True
        try:
            compile_testfile(testprogs_dir, testfile, profile)
            build_fail = False
        except:
            if testfile.endswith("shouldfail.pyxie"):
                print("compilation_tests: AS EXPECTED, COMPILE FAILED FOR", testfile)
            else:
                print("compilation_tests: UNEXPECTED FAILURE FOR FILE", testfile)
                raise

        if not build_fail and testfile.endswith("shouldfail.pyxie"):
            print("compilation_tests: UNEXPECTED BUILD SUCCESS FOR FILE", testfile)
            raise Exception("compilation_tests: UNEXPECTED BUILD SUCCESS FOR FILE %s" % testfile )

        os.chdir(rootdir)

    print("compilation_tests: COMPILING DONE", testprogs)
