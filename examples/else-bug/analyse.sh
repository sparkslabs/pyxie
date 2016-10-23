#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino analyse examples/else-bug/else_bug.pyxie
