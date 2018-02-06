#!/usr/bin/python
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

import os

_default_template = """

using namespace std;

#include <iostream>
#include "iterators.cpp"
template<typename T>
void Print(T x) {
    std::cout << x;
}

void Print() {
    std::cout << std::endl;
}
void DebugFunction() {
    std::cout << "DEBUG FUNCTION CALLED" << std::endl;
}

int main(int argc, char *argv[])
{
%(FRAME_TEXT)s

return 0;
}
"""

_arduino_template = """
#include "iterators.cpp"

void setup()
{
%(FRAME_TEXT)s
}

void loop()
{
}
"""


_default_makefile_template = """
all :
\tg++ %(filename)s.c -o %(filename)s
"""

_arduino_makefile_template = """
BOARD_TAG    = leonardo
ARDUINO_PORT = /dev/ttyACM0
CPPFLAGS = -std=c++11

include /usr/share/arduino/Arduino.mk
"""

def default_result_filename(build_dir, cname):
    result = os.path.join(build_dir, cname)
    return result

def arduino_result_filename(build_dir, cname):
    hexfile = None
    print(os.listdir(build_dir))
    build_sub_dir = "build-leonardo"         # default
    for entry in os.listdir(build_dir):
        if entry.startswith("build-"):
            build_sub_dir = entry
            break
    cbuild_dir = os.path.join(build_dir, build_sub_dir)

    for filename in os.listdir(cbuild_dir):
        if filename.endswith(".hex"):
            hexfile = filename
            break

    if hexfile:
        return os.path.join(cbuild_dir, hexfile)

    # raise Exception("Not Finished")


cpp_templates = {
    "default" : _default_template,
    "arduino" : _arduino_template,
}

makefile_templates = {
    "default" : _default_makefile_template,
    "arduino" : _arduino_makefile_template,
}

mainfile_extensions = {
    "default" : "c",
    "arduino" : "ino",
}

clib_exclusions = {
    "default" : [],
    "arduino" : [],
}

result_file = {
    "default" : default_result_filename,
    "arduino" : arduino_result_filename,

}

modify_result_file = {
    "default": lambda x: x,
    "arduino": lambda x: x+".hex",
}
