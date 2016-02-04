# web/main.py

import sys
from a3web_utils import web_initialize, web_finalize, get_param, set_param, logger

def main():

    retval = 0

    # initialize web
    web_initialize()

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
            logger().info('Act3 Web server is started')

            cherrypy.engine.block()
        except Exception as e:
            logger().error('Page generator is not loaded: %s'%str(e))
            retval = -1
    except ImportError as e:
        logger().error('cherrypy module is not loaded')
        retval = -1

    # finalize web
    web_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())
