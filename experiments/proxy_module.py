#!/usr/bin/python

from __future__ import print_function


class DryrunnableProxyModule(object):
    def __init__(self, module, passthrough=None):
        self.module = module
        self.verbose = True
        self.dryrun = True
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

import os

os.system("ls")
os.chdir("..")
os.system("pwd")
os.chdir("experiments")


p = DryrunnableProxyModule(os,passthrough="popen chdir getcwd".split())
p.dryrun = True

p.system("ls")
x = p.popen("git log|head -20").read()

p.dryrun = False
p.system("ls")



