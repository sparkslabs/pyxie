#!/bin/bash

cd ../..
export PYTHONPATH=.
./bin/pyxie --profile arduino parse examples/analog/analog-serial.pyxie
