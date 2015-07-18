#!/bin/bash


all:
	@echo "make test"
	@echo "make clean"
	@echo "make update"

test:
	rm *~ && g++ iterators_test.cpp -o iterators_test && ./iterators_test

clean:
	rm ./iterators_test

update:
	./mk_py_clib.py