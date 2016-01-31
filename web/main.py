# web/main.py

import sys
from a3web_utils import web_initialize, web_finalize, get_param, set_param, \
    get_param_desc, logger

def find_svc(svcnames):
    if not isinstance(svcnames, list) or len(svcnames)==0 or \
        svcnames[0]=='web': return

    try:
        svcpyroname = get_param('%s:pyroname'%svcnames[0], paramtype='common')
        svc = Pyro4.Proxy(svcpyroname)
        set_param('pyro-%s-object'%svcnames[0], svc, paramtype='runtime')
    except:
        set_param('pyro-%s-object'%svcnames[0], None, paramtype='runtime')
        logger().info('Pyro %s object is not found.'%svcnames[0])

    find_svc(svcnames[1:])

def main():

    retval = 0

    # initialize web
    web_initialize()

    # locate Pyro name server
    try:
        import Pyro4
        ns = None
        try:
            ns = Pyro4.locateNS()
            set_param('pyro-name-object', ns, paramtype='runtime')
            logger().info('Connected to a Pyro name server.')
        except:
            logger().info('Can not connect to a Pyro name server.')
        if ns:
            find_svc(get_param('services', paramtype='common'))
    except ImportError as e:
        logger().warn('Pyro module is not loaded.')
 
    # launch web server
    try:
        import cherrypy
        try:
            cherrypy.config.update({'server.socket_host': '0.0.0.0'})

            from a3web_index import A3Index
            index = A3Index()
            cherrypy.tree.mount(index, '/', index.conf)            

            from a3web_reset import A3Reset
            reset = A3Reset()
            cherrypy.tree.mount(reset, '/reset', reset.conf)            

            cherrypy.engine.start()
            logger().info('Act3 Web server is started.')

            cherrypy.engine.block()
        except Exception as e:
            logger().error('Page generator is not loaded: %s'%str(e))
            retval = -1
    except ImportError as e:
        logger().error('cherrypy module is not loaded.')
        retval = -1

    # finalize web
    web_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())
