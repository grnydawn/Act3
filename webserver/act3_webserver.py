import os
import base64
import shutil
import cherrypy
import Pyro4

HTML_HOME = os.path.dirname(os.path.realpath(__file__))
SESSION_HOME = '%s/session'%HTML_HOME

xformer = None
svcdb = None

def strtohtml(line):
    #dstr = line.decode('utf-8')
    ostr = ''
    for c in line:
        if c==' ':  ostr += '&nbsp;'
        elif c=='\t': ostr += '&nbsp;'*TAB
        elif c=='\n': ostr += '<br>\n'
        else: ostr += c
    return ostr
    #return ostr.encode('utf-8')


class A3WebService(object):

    (UPLOAD, ) = range(1)

    def generate_session(self):
        return base64.b64encode(os.urandom(16), '._')

    @cherrypy.expose
    def index(self):
        # TODO: use cache
        with open('%s/index.html'%HTML_HOME, 'r') as fd:
            return fd.read()

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self, srcfile=None):

        if 'id' not in cherrypy.session:
            cherrypy.session['id'] = self.generate_session()
            # create session on svcdb
            res = svcdb.create_opt_session(cherrypy.session['id'])
            if res['error']: return {'success': 'false', 'msg': 'Can not create session.'}

            # set current stage of the session
            res = svcdb.set_opt_stage(cherrypy.session['id'], self.UPLOAD)
            if res['error']: return {'success': 'false', 'msg': 'Can not set stage.'}
        else:
            # get current stage of the session
            res = svcdb.get_opt_stage(cherrypy.session['id'])
            if res['error']: return {'success': 'false', 'msg': 'Can not get stage.'}

            # check if file upload is valid action on current stage
            if res.has_key('stage') and res['stage']==self.UPLOAD:
                pass
            else:
                print 'BB: ', res
                return {'success': 'false', 'msg': 'Not compatible stage'}

        if srcfile:
            filename = srcfile[0]
            part = srcfile[1]
            
            session_dir = '%s/%s'%(SESSION_HOME, cherrypy.session['id'])
            if not os.path.exists(session_dir):
                os.makedirs(session_dir)
        
            # save file per session
            filepath = '%s/%s'%(session_dir, filename)
            with open(filepath, 'wb') as fd:
                shutil.copyfileobj(part.file, fd)

                # save information on svcdb
                print 'XXX3: ', filepath

            # check file type async

        return {'success': 'true'}

    @cherrypy.expose
    def reset(self):
        if 'id' not in cherrypy.session:
            pass
            #return {'success': 'false', 'msg': 'Session does not exist.'}
        else:
            res = svcdb.reset_opt_session(cherrypy.session['id'])
            if res['error']:
                pass
                #return {'success': 'false', 'msg': 'Can not reset session.'}
            else:
                pass

            print SESSION_HOME, cherrypy.session['id']
            session_dir = '%s/%s'%(SESSION_HOME, cherrypy.session['id'])
            if os.path.exists(session_dir):
                shutil.rmtree(session_dir)

        return self.index()

def start():
    global xformer, svcdb

    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': HTML_HOME
            #TODO: use file to store sessions
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }

    webapp = A3WebService()

    cherrypy.tree.mount(webapp, '/', conf)

    ns = Pyro4.locateNS()
    xformer = Pyro4.Proxy("PYRONAME:act3.xformer")
    svcdb = Pyro4.Proxy("PYRONAME:act3.svcdb")

    if xformer is None or svcdb is None:
        Exception('Can not connect to Xformer or SvcDB')

    cherrypy.engine.start()
    cherrypy.engine.block()

def stop():
    cherrypy.engine.exit()

if __name__ == '__main__':
    start()
