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

from distutils.core import setup
from distutils.version import LooseVersion
import os

def is_package(path):
    return (
        os.path.isdir(path) and
        os.path.isfile(os.path.join(path, '__init__.py'))
        )

def find_packages(path, base="" ):
    """ Find all packages in path """
    packages = {}
    for item in os.listdir(path):
        dir = os.path.join(path, item)
        if os.path.isdir(dir):
            if base:
                module_name = "%(base)s.%(item)s" % vars()
            else:
                module_name = item
            if is_package( dir ):
                packages[module_name] = dir
            packages.update(find_packages(dir, module_name))
    return packages


packages = find_packages(".")
package_names = packages.keys()

setup(name = "pyxie",
      version = "0.0.2",
      description = "Little Python to C++ Compiler",
      url='http://www.sparkslabs.com/michael/',
      author='Michael Sparks (sparkslabs)',
      author_email="sparks.m@gmail.com",
      license='Apache Software License',

      scripts = [
                  'bin/pyxie',
                ],

      packages = package_names,
      package_dir = packages,
      package_data={},
      long_description = """
Little Python to C++ Compiler
"""
      )
