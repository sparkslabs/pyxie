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

# Utility functions

def jdump(thing):
    "Calls __json__ on a thing to try and convert it into a json serialisable thing"
    try:
        return thing.__json__()
    except AttributeError:
        print("WARNING::", repr(thing), "is not a pynode")
        print("       ::", type(thing))


def warn(message):
    if WARNINGS_ARE_FAILURES:
        raise Exception(message)
    else:
        print(message)
