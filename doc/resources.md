## Downloads, Packages, Links, Contacts

### Contact

Michael Sparks : <sparks.m@gmail.com>, [blog](http://www.sparkslabs.com/michael/) [@sparks_rd](http://twitter.com/sparks_rd) [Linked in](https://www.linkedin.com/pub/michael-sparks/0/1b9/a93)

### Blog posts

None exist at present, but when they do, they'll be linked here. See also:

* <http://www.sparkslabs.com/michael/blog/category/pyxie>

### Github

<https://github.com/sparkslabs/pyxie>

### PyPI

<http://pypi.python.org/pypi/pyxie>

### Ubuntu Packages

Ubuntu packages are built for Ubuntu 14.04.02LTS. You can grab them from my PPA here:

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
