#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino analyse examples/servo/servo-test-target.pyxie
