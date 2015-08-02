#!/usr/bin/python

import os
import time
import sys
sys.path[:0] = [".."]

__init__py_source = """\
## Pyxie -- A Little Python to C++ Compiler

{% whatjobdoesthisdo = panel("panels/what-job-does-this-do.md") %}

### Show me something you CAN compile

Currently it can compile very very simple types of python program
that looks like this into an equivalent (simple) C++ program.

{% exampleprogram = panel("panels/example-program_init_py.md") %}

{% whatdoesthisdo = panel("panels/what-does-this-do.md") %}
{% micropython_ref = panel("panels/why-not-micropython.md") %}
In the past I've written a test driven compiler suite, so I'll be following
the same approach here.  It did consider actually making Pyxie use that as a
frontend, but for the moment, I'd like python compatibility.


{% overview_status = panel("panels/overview-status.md") %}

{% influences = panel("panels/overview-influences.md") %}

{% python_version = panel("panels/which-version.md") %}

{% why_write_this = panel("panels/why-write-this.md") %}

{% faq_part_of_larger_project = panel("panels/faq-part-of-larger-project.md") %}

## Release History

Release History:

{% shortlog = panel("panels/shortlog.md") %}

## Language Status

{% shortlog = panel("panels/current-grammar.md") %}

{% grammar = panel("panels/limitations.md") %}

{% grammar = panel("panels/why-python-2-print.md") %}

Michael Sparks, MONTH 2015

"""

__init__py_comment_template = '''\
"""
%s
"""
'''

changelog_header = """\
---
template: mainpage
source_form: markdown
name: Changelog
title: Changelog
updated: %s
---
"""


def pre_run():
    f = open("../CHANGELOG")
    c = f.read()
    f.close()
    now = time.strftime("%B %Y", time.localtime())
    r = changelog_header % now
    f = open("src/changelog.md", "w")
    f.write(r)

    f.write("#")  # Make first heading an h2 not an h1 - due to site related things
    f.write(c)
    f.close()


def get_shortlog_version():
    import pyxie
    doc = pyxie.__doc__
    lines = doc.split("\n")
    while not( lines[0].startswith("Release History:") ):
        lines = lines[1:]

    while not( lines[0].startswith("* ") ):
        lines = lines[1:]

    last_shortlog = lines[0]
    x = last_shortlog.split()
    ver= x[1]

    return ver

def run_local(site_meta, process_directives_callback):  # FIXME: I don't like this callbacks approach

    meta, source_data = site_meta["index.md"],site_meta["index.md"]["_source_data"]

    new_init_py_text = process_directives_callback(__init__py_source)

    new_init_py_text = new_init_py_text.replace("MONTH", time.strftime("%B", time.localtime()) )

    f = open("/tmp/t.tmp", "w")
    f.write(new_init_py_text)
    f.close()

    os.system("pandoc -r markdown /tmp/t.tmp -w rst >/tmp/readme.rst")
    f = open("/tmp/readme.rst")
    rst = f.read()
    f.close()

    os.rename("/tmp/readme.rst", "../README.rst")

    contents = open("../pyxie/__init__.py").read()

    start = contents[:contents.find("#START")+7]     # Wellformed
    contents = contents[contents.find("#START")+7:]  # Wellformed
    body = contents[:contents.find("#END")]          # Wellformed
    contents = contents[contents.find("#END"):]      # Wellformed
    end = contents

    new_body = __init__py_comment_template  % new_init_py_text  # Wellformed

    f = open("../pyxie/__init__.py", "w")   # Wellformed
    f.write( start + new_body + end)        # Wellformed
    f.close()                               # Wellformed

    f = open("setup.tmpl")
    setup_tmpl = f.read()
    f.close()

    ver = get_shortlog_version()

    RST_readme = open("../README.rst").read()
    RST_readme = RST_readme.replace('"""', '\"\"\"')
    setup_py = setup_tmpl.replace("%(VERSION)s", ver)
    setup_py = setup_py.replace("%(REST_PACKAGE_LONG_DESCRIPTION)s", RST_readme)

    f = open("../setup.py","w")
    f.write( setup_py )
    f.close()
