#!/bin/bash

cd ../..
export PYTHONPATH=.

./bin/pyxie --profile arduino compile examples/continuous-servo/servo-test-target.pyxie
