#
# Copyright 2016 Michael Sparks
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from __future__ import print_function

import time

import os as os_

verbose = False
dryrun = False
ver_updating = None

# <Functions to support dry run mode> =====================================
class DryrunnableProxyModule(object):
    """This proxy module is used to stand in front of a bare module, like this:

        import os as os_

        os = DryrunnableProxyModule(os_,passthrough="popen chdir getcwd".split())
        os.verbose = True
        os.dryrun = True

    In this situation you can use "os" as you normally would. The difference however
    is that all calls into the module are now traced - which means we can ber verbose
    about it, or simply not make the calls - to do a dry run.

    For operations that don't mutate external state, you can pass these through
    as per above.

    If you added on the keyword argument "__alwaysdo__" to the call, then the module
    function is always called - whether doing a dryrun or not. This can allow you to
    trace the results of *specific* calls into the library.

    For example:

        import os as os_
        os = DryrunnableProxyModule(os_,passthrough="popen chdir getcwd".split())

        os.verbose = True
        os.dryrun = True

        os.system("ls", __alwaysdo__ = True)

    In this example "ls" would normally NOT be executed without the __alwaysdo__
    argument. Here it will be because it is present.
    """
    def __init__(self, module, passthrough=None):
        self.module = module
        self.verbose = False
        self.dryrun = False
        if passthrough is not None:
            self.passthrough = passthrough[:]
    #
    def __getattr__(self, key):
        if key == "__getattr__":
            return super(DryrunnableProxyModule,self).__getattr__(key)
        result = getattr( self.module, key)
        #
        if callable(result):
            def trace_callable(*argv, **argd):
                do_anyway = False
                do_anyway = do_anyway or (key in self.passthrough)
                if "__alwaysdo__" in argd:
                    do_anyway = True
                    del argd["__alwaysdo__"]
                argv_f = ", ".join([ repr(x) for x in argv])
                argd_f = ", ".join([(x+"="+repr(argd[x])) for x in argd])
                if argd_f != "":
                    argd_f = ", "+argd_f
                if self.dryrun and (not do_anyway):
                    print("DRYRUN:", self.module.__name__ + "." + key +"(" + argv_f + argd_f +")")
                elif self.verbose:
                    print("CALLING:", self.module.__name__ + "." + key +"(" + argv_f + argd_f +")")
                    return result(*argv, **argd)
                else:
                    return result(*argv, **argd)
            return trace_callable
        #
        return result


os = DryrunnableProxyModule(os_,passthrough="popen chdir getcwd".split())

def slurp(filename):
    f = open(filename)
    result = f.read()
    f.close()
    return result


def slurplines(filename):
    f = open(filename)
    result = f.readlines()
    f.close()
    return result

def note(*args):
    if verbose:
        print(" ".join([str(x) for x in args]))

# SYSTEM MUTATOR
def write_file(filename, contents):
    if dryrun:
        print("WOULD WRITE FILE:",filename)
        print("# START CONTENTS ---------------------------------------------- ")
        if verbose:
            for line in contents.split("\n"):
                print("    ",line)
        else:
            c = 0
            for line in contents.split("\n"):
                print("    ",line)
                c += 1
                if c == 15:
                    print("... truncated ... (not verbose)" )
                    break

        print("# END CONTENTS ---------------------------------------------- ")
        return
    elif verbose:
        print("Writing file: ",filename)
    f = open(filename, "wb")
    f.write(contents)
    f.close()

def enable_dryrun():
    global dryrun
    global verbose
    global os

    os.dryrun = dryrun = True

def enable_verbose():
    global dryrun
    global verbose
    global os

    os.verbose = verbose = True

# </Functions to support dry run mode> =====================================


changelog_entry_tmpl = """\
## [%s] - UNRELEASED

### New

*

### What's been fixed?

*

### Internal Changes

*

### Other

*
"""

help_text = """
pyxie-dev [toggles] [options]

toggles:
    -v        verbose mode
    -d        dryrun - don't change files

options:
    get       get current version, and if verbose other information
    propose   get proposed version
    released  get status of released, Returns 0 if released, 1 if not. If verbose outputs state as well
    bump      bump version

    rebase-release Rebase the current code, ready for release
    make-release   Make the release based on current code
    do-upload      upload to launchpad and pypi

pyxie-dev is intended to be run relative to a development checkout
If this is not what you want, set PYXIE_DEV=global prior to running pyxie-dev

eg:
    PYXIE_DEV=global pyxie-dev options"

Expected usage:

Before a release:

    - Create a branch containing the history. (eg git checkout -b pre_v0.0.19)
    - Checkout WIP again
    - Then: ./bin/pyxie-dev rebase-release
       - Clean up your history as you see fit
    - Then: ./bin/pyxie-dev make-release
    - Assuming that went fine, add/commit all the changes made for the release to git
    - Then: ./bin/pyxie-dev do-upload
    - Then double check everything related to that release is committed and push.

    - NOTE: When pushing, remember to push the tags - git push --follow-tags so that
      the release shows up on github.

You may need to do a stash/fetch/rebase/stash pop/build_site.py on the webserver

After a release:

    - Update latest release info in site/src/index.md (this will get rolled in make-release)
    - You may need to do a stash/fetch/rebase/stash pop/build_site.py on the webserver
    - Check the version you've just released has been released:
      - ./bin/pyxie-dev get
      - ./bin/pyxie-dev released
    - Check the next version looks sane:
      - ./bin/pyxie-dev propose
    - If it does, bump versions:
      - ./bin/pyxie-dev bump

Note:
    - Once the new build of the package appears on launchpad, do the following:

    cd ~/Tools/ubuntu-archive-tools
    ./copy-package --from=~sparkslabs/ubuntu/packages --from-suite=xenial --to=~sparkslabs/ubuntu/packages --to-suite=precise -b -y pyxie
    ./copy-package --from=~sparkslabs/ubuntu/packages --from-suite=xenial --to=~sparkslabs/ubuntu/packages --to-suite=trusty -b -y pyxie
    ./copy-package --from=~sparkslabs/ubuntu/packages --from-suite=xenial --to=~sparkslabs/ubuntu/packages --to-suite=vivid -b -y pyxie
    ./copy-package --from=~sparkslabs/ubuntu/packages --from-suite=xenial --to=~sparkslabs/ubuntu/packages --to-suite=wily -b -y pyxie
    ./copy-package --from=~sparkslabs/ubuntu/packages --from-suite=xenial --to=~sparkslabs/ubuntu/packages --to-suite=yakkety -b -y pyxie

    This will make the package available for older releases (and the current non-LTS releases)

"""

def confirm_release_summary_with_user(proposed_release_summary):
    while True:
        print("Proposed_release_summary is this:", proposed_release_summary )
        print("Are you happy with this?")
        answer = raw_input("> ")
        answer = answer.lower()
        if answer.startswith("y"):
            break
        print("OK, enter a new one line release summary")
        proposed_release_summary  = raw_input("> ")
        proposed_release_summary  = proposed_release_summary .strip()

    return proposed_release_summary


# INFO EXTRACTOR
def get_latest_git_shortlog():
    # Extract Shortlog
    x = os.popen("git log|head -20").read()
    lines = x.split("\n")
    latest_shortlog = lines[4].strip()
    return latest_shortlog


# INFO EXTRACTOR
def get_shortlog_version(shortlogfile):
    global ver_updating

    shortlog = [x.strip() for x in slurplines(shortlogfile) ]

    if shortlog[0] != "---":
        print("CANNOT GET VERSION")
        print("\n".join(shortlog))
        return "-1", "UNRELEASED"

    log = shortlog[1:]
    while log[0] != "---":
        log = log[1:]

    current_version_info = log[1].split()

    ver, release_date = current_version_info[1], current_version_info[3]

    if ver_updating is None:
        ver_updating = ver

    return ver, release_date

# INFO EXTRACTOR
def unreleased(release):
    return release == "UNRELEASED"


# INFO EXTRACTOR
def get_next_version(ver_type):
    note("get_next_version", ver_type)
    ver, release = get_shortlog_version("site/src/panels/shortlog.md")

    major,minor,patch = [ int(x) for x in ver.split(".") ]
    if ver_type == "major":
        major = major + 1
    elif ver_type == "minor":
        minor = minor + 1
    else:
        patch = patch +1

    new_version = "%d.%d.%d" % (major, minor, patch)
    return new_version, release



# SYSTEM MUTATOR - UDPDATED - OK
def rebuild_docs():
    print("rebuild_docs")

    here = os.getcwd()
    os.chdir("site")
    os.system("./build_site.py")
    os.chdir(here)


# SYSTEM MUTATOR - UPDATED -OK
def tag_release():
    print("tag_release")

    os.system("rm -rf dist")
    os.system("rm MANIFEST")
    ver,release = get_shortlog_version("site/src/panels/shortlog.md")
    os.system('git tag -a v%s -m "Version %s"' % (ver, ver) )

# SYSTEM MUTATOR - UPDATED -OK
def update_python_version_of_the_clib():
    # Update python version of the clib.
    here = os.getcwd()
    os.chdir("clib")
    os.system("./mk_py_clib.py")
    os.chdir(here)

# SYSTEM MUTATOR - UPDATED -OK
def upload_to_launchpad():
    # Build debian package - for actual release change "make deb" to "make ppadeb"
    os.system("rm -rf dist")
    os.system("rm MANIFEST")
    os.system("make ppadeb")
    os.system("make distclean")

# SYSTEM MUTATOR - UPDATED -OK
def upload_to_pypi():
    # Build PyPI release
    os.system("rm -rf dist")
    os.system("rm MANIFEST")
    os.system("python setup.py sdist upload")
    os.system("make distclean")

# <NEED REFACTOR PROBABLY> ------------------------------------------------------


#  - UPDATED -OK
def bump_shortlog(new_ver):
    shortlog =  slurplines("site/src/panels/shortlog.md")

    result = []

    newline = "* %s - UNRELEASED - TBD\n" % (new_ver,)
    shortlog.insert(7, newline)

    for line in shortlog:
        result.append(line)

    write_file("site/src/panels/shortlog.md","".join(result))


# SYSTEM MUTATOR  - UPDATED -OK
def update_current_shortlog(shortlog_entry):
    # Update shortlog with proposed_release_summary

    ver, release = get_shortlog_version("site/src/panels/shortlog.md")
    if not unreleased(release):
        print("We appear to already have released this release.")
        print("release date:", release)
        #FIXME: Surely we should abort the release then?

    release_date = time.strftime("%Y-%m-%d")
    new_log_line = "* %s - %s - %s\n" % (ver, release_date, shortlog_entry)

    shortlog =  slurplines("site/src/panels/shortlog.md")

    result = []

    for line in shortlog:
        if (ver in line) and ("UNRELEASED") in line:
            result.append(new_log_line)
        else:
            result.append(line)
    write_file("site/src/panels/shortlog.md", "".join(result))



# SYSTEM MUTATOR - UPDATED - OK
def bump_CHANGELOG(new_ver):
    note("TBD -- bump_CHANGELOG")

    lines = slurplines("CHANGELOG")

    old_ver = ver_updating

    for line in range(len(lines)):
        if old_ver in lines[line]:
            # print("FOUND START OF LAST VERSION")
            break

    new_changelog = changelog_entry_tmpl % new_ver
    lines[line:line] = [x+"\n" for x in new_changelog.split("\n") ]

    write_file("CHANGELOG", "".join(lines))


# SYSTEM MUTATOR - UPDATED - OK
def bump_Makefile(ver):
    note("TBD -- bump_Makefile") 

    lines = slurplines("Makefile")

    result = []

    for line in lines:
        if line.startswith("VERSION="):
            result.append("VERSION=%s\n" % (ver,)  )
        else:
            result.append(line)


    write_file("Makefile", "".join(result))


# SYSTEM MUTATOR - UPDATED - OK
def bump_rebuildDocs():
    note("TBD -- bump_rebuildDocs")

    here = os.getcwd()
    os.chdir("site")
    os.system("./build_site.py")
    os.chdir(here)

# SYSTEM MUTATOR - UPDATED - OK
def update_changelog_release_date():
    print("UPDATE CHANGELOG")

    release_date = time.strftime("%Y-%m-%d")

    lines = slurplines("CHANGELOG")
    result = []


    found = False
    for line in lines:
        if ("UNRELEASED" in line) and not found:
            line = line.replace("UNRELEASED",release_date)
            found = True
        result.append(line)

    write_file("CHANGELOG", "".join(result))

# </NEED REFACTOR PROBABLY> ------------------------------------------------------


# ================================================================== EXTERNAL API

# INFO EXTRACTOR - UPDATED - OK
# EXTERNAL API
def do_usage():
    current_version = get_shortlog_version("site/src/panels/shortlog.md")

    print(help_text)
    print("CURRENT VERSION:", current_version)

# INFO EXTRACTOR - UPDATED - OK
# EXTERNAL API
def do_get():
    ver, release = get_shortlog_version("site/src/panels/shortlog.md")
    note("Dryrun: ", dryrun)
    note("Release date:", release)
    note("Version:")

    print(ver)
    return 0


# INFO EXTRACTOR - UPDATED - OK
# EXTERNAL API
def do_released():
    note("do_released")
    ver, release = get_shortlog_version("site/src/panels/shortlog.md")
    if unreleased(release):
        note("Unreleased")
        return 1
    note("Released:", release)
    note("Version:", ver)

    return 0


# SYSTEM MUTATOR - UPDATED - OK
# EXTERNAL API
def do_bump(ver_type):
    global dryrun
    global verbose
    note("bump", ver_type)

    nobump = False
    ver, release = get_next_version(ver_type)
    if unreleased(release):
        print("Refusing to bump release version until this version is released")
        print("You can still do this manually, if you must")
        print()
        print("So that you can see what would be updated though, switching dryrun to True, and verbose to True")
#        os.dryrun = dryrun = True
#        os.verbose = verbose = True
        enable_dryrun()
#        enable_verbose()


        nobump = True

    bump_shortlog(ver)
    bump_CHANGELOG(ver)
    bump_Makefile(ver)
    bump_rebuildDocs()

    if nobump:
        note("NOTE: We did not actually bump the release")
        return 1


# INFO EXTRACTOR - UPDATED - OK
# EXTERNAL API
def do_propose(ver_type):
    note("propose", ver_type)
    ver, release = get_next_version(ver_type)
    if unreleased(release):
        print("Release current version -", ver, "- before bumping to next release")
        return 1

    print("PROPOSED NEW VERSION:", ver)
    return 0


# UPDATED - OK
# EXTERNAL API
def rebase_release():
    release_branch = time.strftime("%Y%m%d")

    os.system("git checkout -b "+release_branch)
    os.system("git checkout WIP")
    os.system("git rebase -i master")

    return 0


# SYSTEM MUTATOR - UPDATED - OK
# EXTERNAL API
def make_release():

    proposed_release_summary = get_latest_git_shortlog()
    release_summary = confirm_release_summary_with_user(proposed_release_summary)

    update_current_shortlog(release_summary)

    # Update changelog date (assume rest is up to date)
    update_changelog_release_date()
    rebuild_docs()
    tag_release()

    update_python_version_of_the_clib()

    return 0


# - UPDATED -OK
# EXTERNAL API
def do_upload():

    upload_to_launchpad()
    upload_to_pypi()


def main(argv):
    if "-v" in argv:
        enable_verbose()
        argv = [x for x in argv if x != "-v" ]

    if "-d" in argv:
        enable_dryrun()
        argv = [x for x in argv if x != "-d" ]

    if len(argv) == 2:
        if argv[1] == "get":
            return do_get()

        if argv[1] == "released":
            return do_released()

    if len(argv) >= 2:
        if argv[1] == "bump":
            if len(argv) == 3:
                ver_type = argv[2]
            else:
                ver_type = "patch"
            return do_bump(ver_type)

        if argv[1] == "propose":
            if len(argv) == 3:
                ver_type = argv[2] 
            else:
                ver_type = "patch"
            return do_propose(ver_type)

        if argv[1] == "rebase-release":
            rebase_release()
            return 0

        if argv[1] == "make-release":
            make_release()
            return 0

        if argv[1] == "do-upload":
            do_upload()
            return 0

    do_usage()
    return 1
