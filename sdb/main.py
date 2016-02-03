# sdb/main.py

import sys
import time

from a3sdb_utils import sdb_initialize, sdb_finalize, get_param, set_param, logger
from a3sdb_pyro import A3SdbPyroIF

def main():

    retval = 0

    # initialize sdb
    sdb_initialize()

    # locate Pyro name server
    try:
        import Pyro4
        daemon = Pyro4.Daemon()
        sdbobj = A3SdbPyroIF()
        sdb_uri = daemon.register(sdbobj)

        ns = None
        for i in range(get_param('name:search_maxtries')):
            try: ns = Pyro4.locateNS()
            except: pass
            if ns: break
            time.sleep(get_param('name:search_interval'))

        if ns:
            set_param('pyro-name-object', ns)
            ns.register("sdb", sdb_uri)
            logger().info('sdb is registered on a Pyro name server.')
            daemon.requestLoop()
            retval = 0
    except ImportError as e:
        logger().warn('sdb is not registered on a Pyro name server.')
        retval = -1

    # finalize web
    sdb_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())

