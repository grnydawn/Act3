import cherrypy
      
class HelloWorld(object):
    def index(self):
        return "Hello World!"
    index.exposed = True

def start():
    cherrypy.quickstart(HelloWorld())
