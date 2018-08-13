# Note: we instantiate the same 'cffi.FFI' class as in the previous
# example, but call the result 'ffibuilder' now instead of 'ffi';
# this is to avoid confusion with the other 'ffi' object you get below

from cffi import FFI
import sys
import subprocess
ffibuilder = FFI()

if sys.platform == 'win32':
    objects = ['./nng/build/Debug/nng.lib']
    # libraries determined to be necessary through trial and error
    libraries = ['Ws2_32', 'Advapi32']
else:
    objects = ['./nng/build/libnng.a']
    libraries = []


ffibuilder.set_source("pynng._nng",
   r""" // passed to the real C compiler,
        // contains implementation of things declared in cdef()
        #define NNG_DECL
        #include <nng.h>
        #include <protocol/bus0/bus.h>
        #include <protocol/pair0/pair.h>
        #include <protocol/pair1/pair.h>
        #include <protocol/pipeline0/pull.h>
        #include <protocol/pipeline0/push.h>
        #include <protocol/pubsub0/pub.h>
        #include <protocol/pubsub0/sub.h>
        #include <protocol/reqrep0/req.h>
        #include <protocol/reqrep0/rep.h>
        #include <protocol/survey0/respond.h>
        #include <protocol/survey0/survey.h>


    """,
    libraries=libraries,
    # library_dirs=['nng/build/Debug',],
    # (more arguments like setup.py's Extension class:
    include_dirs=['nng/src'],
    extra_objects=objects,
)

with open('nng_api.h') as f:
   api = f.read()
ffibuilder.cdef(api)

if __name__ == "__main__":
    ffibuilder.compile(verbose=True)
