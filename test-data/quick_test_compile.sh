#!/bin/bash

UNDERTEST=`cat under_test` 
cd ..
PYTHONPATH=. ./bin/pyxie compile test-data/progs/$UNDERTEST

