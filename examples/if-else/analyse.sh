#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino analyse examples/if-else/if_else.pyxie
