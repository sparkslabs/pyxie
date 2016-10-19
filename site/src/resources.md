---
template: mainpage
source_form: markdown
name: Downloads, Links, etc
updated: October 2016 (with release 0.1.23)
title: Downloads, Packages, Links, Contacts, Resources, etc
---
## Downloads, Packages, Links, Contacts

### Contact

Michael Sparks : <sparks.m@gmail.com>, [blog](http://www.sparkslabs.com/michael/) [@sparks_rd](http://twitter.com/sparks_rd) [Linked in](https://www.linkedin.com/pub/michael-sparks/0/1b9/a93)

### Blog posts

See:

* <http://www.sparkslabs.com/michael/blog/category/pyxie>

(If you write something, let me know and I'll add a link)

## Code

The recommended way of working with pyxie as a user is via ubuntu packages.
The recommended way of working with the source is via a github checkout, and
using "make devloop" to check what things are like when installed on a debian
based system. (That way things are always checked from within a package)
Pull requests welcome.

However these modes of working won't suit everyone so below is a bit more
detailed than that!


### Github

<https://github.com/sparkslabs/pyxie>

### PyPI

<http://pypi.python.org/pypi/pyxie>

### Installation from source:

#### Manual

Usual approach - get the source, then:

    sudo python setup.py install

#### Pip

Usual approach - get the package:

    sudo pip install pyxie

#### Debian Package

Again get the source, then:

    make deb
    make use

(Requires py2dsc to be installed)

Also, you can purge what's currently installed and build a fresh clean
package and use that by doing this:

    make devloop


### Ubuntu Packages

#### Ubuntu versions

Ubuntu packages are built for Ubuntu LTS versions:

* 16.04 (xenial) (main development environment)
* 14.04 (trusty)
* 12.04 (precise)

The following versions of ubuntu are also backported/forward ported to:
* 16.10 (yakkety)
* 15.10 (wily)
* 15.04 (vivid)

Utopic and other versions aren't here because launchpad can't generate those trivially, 
largely because Ubuntu cease support after given time periods

#### Getting them

You can grab them from my PPA here.

* <https://launchpad.net/~sparkslabs/+archive/ubuntu/packages>

Add my PPA:

    sudo add-apt-repository ppa:sparkslabs/packages

Update:

    sudo apt-get update

Install:

    sudo apt-get install python-pyxie

Use:

    $ pyxie

    pyxie -- A little python compiler
    Usage:

        pyxie -- show runtime arguments
        pyxie --test run-tests -- Run all tests
        pyxie --test parse-tests -- Just run parse tests
        pyxie --test compile-tests -- Just run compile tests
        pyxie --test parse filename -- Parses a given test given a certain filename
        pyxie parse filename -- parses the given filename, outputs result to console
        pyxie analyse filename -- analyses the given filename, outputs result to console
        pyxie compile path/to/filename.suffix -- compiles the given file to path/to/filename
        pyxie compile path/to/filename.suffix  path/to/other/filename -- compiles the given file to the destination filename
