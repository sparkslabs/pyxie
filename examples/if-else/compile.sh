#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino compile examples/if-else/if_else.pyxie
