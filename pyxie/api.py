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

"""
NOTE WELL: This file is an initial public API for using Pyxie in a progammatic context.

This is a pre-alpha public API, names are likely to change slightly because they
make slightly less sense in this context

It should be noted that this is based on what has been (until moving here) in bin/pyxie
as an internal API used for the Pyxie front end. It is moved here in case you wish to
call pyxie directly from an application, but not by "calling" the main script.

I am NOT clear at this instant if this is a good idea or a bad idea.

Feedback on this would be a good idea.

API:

    from pyxie.api import initialise_API
    from pyxie.api import set_profile
    from pyxie.api import PyxieAPI

    initialise_API(profile="default")
        # Initialises the API - must be called before the other options

    set_profile(profile_name)
        # If after using the API you decide you want to change the profile, you can,
        # using this option.


    PyxieAPI.parse(filename)
        # parses the given filename, outputs result to console

    PyxieAPI.analyse(filename)
        # parses and analyses the given filename, outputs result to console

    PyxieAPI.codegen(filename, result_filename=None)
        # parses, analyse and generate code for the given filename, outputs result
        # to console. Does not attempt compiling

    PyxieAPI.compile(filename, result_filename=None)
        # compiles the given file.
        # for a given file "some/program.pyxie" it is compiled to "some/program"
        # result_filename can be provide an alternative output name

-- November 2016, Michael

"""
from __future__ import print_function
from __future__ import absolute_import

__all__ = [ "initialise_API",   # You should call this with a profile name
            "StandardOptions",  # These are the primary methods you will want
            "TestsLauncher",    # You may want to call these
            "set_profile"       # You can use this to change the profile name you're using.
            ]

__API_VERSION__ = "0.1" # Only increases when necessary - matches MAJOR/MINOR for project
__API_MAJOR__ = 0
__API_MINOR__ = 1

import pprint

import pyxie.parsing.context

from pyxie.core import parse_file
from pyxie.core import analyse_file
from pyxie.core import compile_file
from pyxie.core import convert_file
from pyxie.core import codegen_phase
from pyxie.core import compilation_tests
from pyxie.core import compile_testfile
from pyxie.core import parsing_tests
from pyxie.core import parse_testfile
from pyxie.core import testprogs_dir


# This is to support compilation profiles. This may or may not turn out to
# be a good approach.  (#3/#3.x)
profile = "default"

def set_profile(profile_name):
    global profile
    print("USING PROFILE: ", profile)
    profile = profile_name


# The purpose of this command line dispatcher is to simplify options handling at the
# expense of being a bit pickier about it.

class CommandLineDispatcher(object):
    @classmethod
    def handles(klass, command):
        return  command.replace("-","_") in [ x for x in dir(klass) if not(x.startswith("_"))]
    #
    @classmethod
    def handle(klass, command, *args):
        f = getattr(klass, command.replace("-","_"))
        f(*args)


class TestsLauncher(CommandLineDispatcher):
    @staticmethod
    def run_tests():
        """Run all tests"""
        parsing_tests()
        compilation_tests(profile)

    @staticmethod
    def parse_tests():
        """Just run parse tests"""
        parsing_tests()

    @staticmethod
    def compile_tests():
        """Just run compile tests"""
        compilation_tests(profile)

    @staticmethod
    def parse(filename):
        """Parses a given test given a certain filename"""
        AST = parse_testfile(testprogs_dir, filename)
        pprint.pprint(AST)
        pprint.pprint(AST.__json__())

    @staticmethod
    def compile(filename):
        """Parses a given test given a certain filename"""
        compile_testfile(testprogs_dir, filename, profile)


class StandardOptions(CommandLineDispatcher):
    @staticmethod
    def parse(filename):
        """parses the given filename, outputs result to console"""
        AST = parse_file(filename)
        pprint.pprint(AST)
        pprint.pprint(AST.__json__())
        if 0:
            import json
            print("Also writing a copy to ", filename+".json")
            f = open(filename+".json", "w")
            f.write(json.dumps(AST.__json__()))
            f.close()

    @staticmethod
    def analyse(filename):
        """parses and analyse the given filename, outputs result to console"""
        analyse_file(filename)

    @staticmethod
    def codegen(filename, result_filename=None):
        """parses, analyse and generate code for the given filename, outputs result to console. Does not attempt compiling"""
        codegen_phase(filename, result_filename, profile)

    @staticmethod
    def compile(filename, result_filename=None):
        """compiles the given file to path/to/filename -- result_filename can be provide an alternative output name"""
        compile_file(filename, profile, result_filename)
    
    @staticmethod
    def convert(filename, result_filename=None):
        """converts the given file to cpp code but does not compile"""
        convert_file(filename, profile, result_filename)


def initialise_API(profile_name):
    # Create a default profile - whether or not it is used.
    print("CREATING A CONTEXT")
    context = pyxie.parsing.context.Context()
    context.tag = "PROFILE: "+ profile_name

    if profile_name == "arduino":
        from pyxie.profile.arduino import initialise_profile
        initialise_profile(context)

    elif profile_name == "default":
        # No profile, no profile specific initialisation
        pass

    else:
        print("UNKNOWN PROFILE")
        context.tag = "PROFILE:"+profile_name

    pyxie.parsing.context.profile_context = context
    set_profile(profile_name)


PyxieAPI = StandardOptions   # Alias StandardOptions, but allows us to change the API if necessary
