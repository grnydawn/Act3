# web/main.py

import sys

def main():
    from a3web_utils import a3web_initialize, a3web_finalize, get_param, set_param, \
        get_param_desc, get_logger

    retval = 0

    # initialize a3web
    a3web_initialize()

    # locate Pyro name server
    try:
        import Pyro4
        try:
            ns = Pyro4.locateNS()
            set_param('pyro-nameserver-object', ns, paramtype='runtime')
            get_logger().info('Connected to a Pyro name server.')
            try:
                xfpyroname = get_param('xformer:pyroname', paramtype='a3common')
                xformer = Pyro4.Proxy(xfpyroname)
            except:
                set_param('pyro-xformer-object', None, paramtype='runtime')
                get_logger().warn('Pyro xformer object is not found.')
        except:
            set_param('pyro-nameserver-object', None, paramtype='runtime')
            get_logger().warn('Can not connect to a Pyro name server.')
    except ImportError as e:
        get_logger().warn('Pyro module is not loaded.')
 
    # launch web server
    try:
        import cherrypy
        try:
            from a3web_index import A3Index
            index = A3Index()
            cherrypy.tree.mount(index, '/', index.conf)            

            cherrypy.engine.start()
            get_logger().info('Act3 Web server is started.')

            cherrypy.engine.block()
        except Exception as e:
            get_logger().error('Index page generator is not loaded.')
            retval = -1
    except ImportError as e:
        get_logger().error('cherrypy module is not loaded.')
        retval = -1

    # finalize a3web
    a3web_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())
