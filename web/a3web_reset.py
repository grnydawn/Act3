# a3web_index.py

import cherrypy

from a3web_utils import SCRIPT_DIR

class A3Reset(object):
    def __init__(self):
        self.conf = \
        {
            '/':
            {
                'tools.sessions.on': True,
                'tools.staticdir.root': SCRIPT_DIR
            },
            '/static':
            {
                'tools.staticdir.on': True,
                'tools.staticdir.dir': './public'
            }
        }

    @cherrypy.expose
    def index(self):
        with open('%s/index.html'%SCRIPT_DIR, 'r') as fd:
            return fd.read()
