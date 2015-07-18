#!/usr/bin/python

import os
import pprint
files = {}
for libfilename in os.listdir("."):
    if not( libfilename.endswith("cpp") or libfilename.endswith("hpp")):
        continue
    print "OK, Adding libfilename", libfilename

    f = open(libfilename)
    source = f.read()
    f.close()
    files[libfilename]=source


template = """\
#!/usr/bin/python

files = %s

"""

print "Deploying into ../pyxie/codegen/clib.py"
clib = template % repr(files)
d = open("../pyxie/codegen/clib.py","w")
d.write(clib)
d.close()