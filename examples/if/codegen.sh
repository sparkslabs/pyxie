#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino codegen examples/if/if.pyxie
