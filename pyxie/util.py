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

# Utility functions extracted from elsewhere

import pyxie.transform.simple_cpp

def todo(*args):
    print("TODO", " ".join([repr(x) for x in args]))

def get_blank_line():
    return pyxie.transform.simple_cpp.get_blank_line()

def Print(*args):
    return pyxie.transform.simple_cpp.Print(*args)
