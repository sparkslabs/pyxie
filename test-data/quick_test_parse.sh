#!/bin/bash

UNDERTEST=`cat under_test` 
cd ..

PYTHONPATH=. ./bin/pyxie parse test-data/progs/$UNDERTEST
