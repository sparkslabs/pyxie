---
template: mainpanel
source_form: markdown
name: Why a python 2 print statement?
updated: July 2015
title: Why a python 2 print statement?
---
## Why a python 2 print statement?

Python 2 has print statement with special notation; python 3's version is
a function call. The reason why this grammar currently has a python-2 style
print statement with special notation is to specifically avoid implementing
general function calls yet. Once those are implemented, special cases - like
implementing print - can be implemented, and this python 2 style print
statement WILL be removed. I expect this will occur around version 0.0.15,
based on current rate of progress.

Keeping it for now also simplifies "yield" later