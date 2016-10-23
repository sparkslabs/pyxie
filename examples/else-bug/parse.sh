#!/bin/bash

cd ../..
export PYTHONPATH=.
./bin/pyxie --profile arduino parse examples/else-bug/else_bug.pyxie
