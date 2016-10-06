#!/bin/bash

UNDERTEST=`cat under_test` 
cd ..

PYTHONPATH=. ./bin/pyxie analyse test-data/progs/$UNDERTEST
