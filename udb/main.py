# udb/main.py

import sys
import time

from a3udb_utils import udb_initialize, udb_finalize, get_param, set_param, logger
from a3udb_pyro import A3UdbPyroIF

def main():

    retval = 0

    # initialize udb
    udb_initialize()

    # locate Pyro name server
    try:
        import Pyro4
        daemon = Pyro4.Daemon()
        udbobj = A3UdbPyroIF()
        udb_uri = daemon.register(udbobj)

        ns = None
        for i in range(get_param('name:search_maxtries')):
            try: ns = Pyro4.locateNS()
            except: pass
            if ns: break
            time.sleep(get_param('name:search_interval'))

        if ns:
            set_param('pyro-name-object', ns)
            ns.register("udb", udb_uri)
            logger().info('udb is registered on a Pyro name server')
            daemon.requestLoop()
            retval = 0
    except ImportError as e:
        logger().warn('udb is not registered on a Pyro name server')
        retval = -1

    # finalize web
    udb_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())

