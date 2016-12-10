#!/bin/bash

FILE=neo-simple.pyxie

cd ../..
export PYTHONPATH=.
./bin/pyxie --profile arduino parse examples/neopixel/$FILE

