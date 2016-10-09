#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino analyse examples/puppy/puppy-min.pyxie
