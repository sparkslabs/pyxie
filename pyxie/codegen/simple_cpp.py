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

from __future__ import print_function
from __future__ import absolute_import

from pyxie.model.cppnodes import CppProgram

blank_line = ""
source = []

def Print(*args):
    y = " ".join([str(x) for x in args])
    source.append(y)


def get_blank_line():
    return blank_line


def reset_parser():
    global source
    source = []


# def build_program(json):
#     json = CppProgram.fromjson(json)
