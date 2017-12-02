#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino compile examples/pass/pass.pyxie
