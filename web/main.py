# web/main.py

import os
import sys
import time

ACT3_HOME = '%s/..'%os.path.dirname(os.path.realpath(__file__))
COMMON_DIR = ACT3_HOME + '/common'
if COMMON_DIR not in sys.path:
    sys.path.insert(0, COMMON_DIR)

from a3web_utils import web_initialize, web_finalize, get_param, set_param, \
    logger

def find_svc(svcnames):
    if not isinstance(svcnames, list) or len(svcnames)==0 or \
        svcnames[0]=='web': return

    try:
        svc = Pyro4.Proxy('PYRONAME:%s'%svcnames[0])
        set_param('pyro-%s-object'%svcnames[0], svc)
    except:
        set_param('pyro-%s-object'%svcnames[0], None)
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
        for i in range(get_param('name:search_maxtries')):
            try:
                ns = Pyro4.locateNS()
                set_param('pyro-name-object', ns)
                logger().info('Connected to a Pyro name server.')
                break
            except:
                time.sleep(get_param('name:search_interval'))
        if ns:
            find_svc(get_param('services'))
        else:
            logger().info('Can not connect to a Pyro name server.')
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

            from a3web_upload import A3Upload
            upload = A3Upload()
            cherrypy.tree.mount(upload, '/upload', upload.conf)            

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
