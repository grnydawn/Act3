# a3web_subscribe.py

import os
import cherrypy

from a3web_utils import SCRIPT_DIR, generate_session, pyrocall, logger

class A3Subscribe(object):
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
    @cherrypy.tools.json_out()
    def index(self, username=None, password=None):
        retval = {'success': 'false', 'msg': []}

        # if session does not exist, create one
        if 'id' not in cherrypy.session:
            cherrypy.session['id'] = generate_session()

            # create session on svcdb
            res = pyrocall('sdb', 'create_opt_session', cherrypy.session['id'])
            if res['error']: retval['msg'].append(res['msg'])

        print('XXXX', username, password)
        if username and password:
            res = pyrocall('udb', 'subscribe', cherrypy.session['id'], username, password)
            if res['error']: retval['msg'].append(res['msg'])
            retval['success'] = 'true'
        else:
            retval['msg'].append('Subscription is failed.')

        return retval
