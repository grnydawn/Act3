# xform/main.py

import sys
import time

from a3xform_utils import xform_initialize, xform_finalize, get_param, set_param, logger
from a3xform_pyro import A3SdbPyroIF
from a3xform_ordermgr import A3OrderMgr

def main():

    retval = 0

    # initialize xform
    xform_initialize()
    set_param('order-mgr', A3OrderMgr())

    # locate Pyro name server
    try:
        import Pyro4
        daemon = Pyro4.Daemon()
        xformobj = A3SdbPyroIF()
        xform_uri = daemon.register(xformobj)

        ns = None
        for i in range(get_param('name:search_maxtries')):
            try: ns = Pyro4.locateNS()
            except: pass
            if ns: break
            time.sleep(get_param('name:search_interval'))

        if ns:
            set_param('pyro-name-object', ns)
            ns.register("xform", xform_uri)
            logger().info('xform is registered on a Pyro name server')
            daemon.requestLoop()
            retval = 0
    except ImportError as e:
        logger().warn('xform is not registered on a Pyro name server')
        retval = -1

    # finalize web
    xform_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())

