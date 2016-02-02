# sdb/main.py

import sys
import time

from a3sdb_utils import sdb_initialize, sdb_finalize, get_param, set_param, logger

def find_svc(svcnames):
    if not isinstance(svcnames, list) or len(svcnames)==0 or \
        svcnames[0]=='sdb': return

    try:
        svc = Pyro4.Proxy('PYRONAME:%s'%svcnames[0])
        set_param('pyro-%s-object'%svcnames[0], svc)
    except:
        set_param('pyro-%s-object'%svcnames[0], None)
        logger().info('Pyro %s object is not found.'%svcnames[0])

    find_svc(svcnames[1:])

def main():

    retval = 0

    # initialize sdb
    sdb_initialize()

    # locate Pyro name server
    try:
        import Pyro4
        daemon = Pyro4.Daemon()
        sdb = get_param('pyro-sdb-object')
        sdbpyro = daemon.register(sdb)
        ns = None
        for i in range(get_param('name:search_maxtries')):
            try:
                ns = Pyro4.locateNS()
                set_param('pyro-name-object', ns)
                logger().info('Connected to a Pyro name server.')
                break
            except:
                time.sleep(get_param('name:search_interval'))
        if ns:
            ns.register('sdb', sdbpyro)
            find_svc(get_param('services'))
            daemon.requestLoop()
        else:
            logger().info('Can not connect to a Pyro name server.')
    except ImportError as e:
        logger().warn('Pyro module is not loaded.')

    # finalize web
    sdb_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())

