#!/usr/bin/python
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
      version = "0.0.1",
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
