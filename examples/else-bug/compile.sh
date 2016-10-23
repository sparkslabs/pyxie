#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino compile examples/else-bug/else_bug.pyxie
