#!/bin/bash

FILE=arduino-blink.pyxie
# FILE=arduino-for-blink.pyxie

cd ../..
export PYTHONPATH=.
./bin/pyxie --profile arduino analyse examples/arduino/$FILE

