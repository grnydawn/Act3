import os
import cherrypy

HTML_HOME = os.path.dirname(os.path.realpath(__file__))

class A3WebService(object):
    def index(self):
        with open('%s/index.html'%HTML_HOME, 'r') as fd:
            return fd.read()
    index.exposed = True

def start():

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': HTML_HOME
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    webapp = A3WebService()

    cherrypy.tree.mount(webapp, '/', conf)

    #ns = Pyro4.locateNS()
    #order_mgr = Pyro4.Proxy("PYRONAME:kvec.order_mgr")

    cherrypy.engine.start()
    cherrypy.engine.block()

def stop():
    cherrypy.engine.exit()

if __name__ == '__main__':
    start()
