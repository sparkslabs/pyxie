#!/bin/bash

FILE=neo-simple.pyxie

cd ../..
export PYTHONPATH=.
./bin/pyxie --profile arduino compile examples/neopixel/$FILE
