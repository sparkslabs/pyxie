#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino analyse examples/while-continue/while-continue.pyxie
