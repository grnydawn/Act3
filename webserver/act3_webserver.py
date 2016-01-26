import os
import base64
import shutil
import cherrypy
import Pyro4
from act3_common import pyrocall

HTML_HOME = os.path.dirname(os.path.realpath(__file__))
WS_SESSION_HOME = '%s/session'%HTML_HOME

ws_globals = {'svcdb': None, 'xformer': None, 'localcomp': None}

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
    def collect(self, os_text=None, build_text=None, run_text=None):
        retval = {'success': 'false'}

        # check os_text, build_text, and run_text
        if any( item is None for item in [os_text, build_text, run_text]):
            return retval

        order_flags = '--build_cmd "%s" --run_cmd "%s"'%(build_text, run_text)
        session_dir = '%s/%s'%(WS_SESSION_HOME, cherrypy.session['id'])
        # order work 
        res = pyrocall(ws_globals['localcomp'].run, cherrypy.session['id'], 'ref_timing', \
            session_dir, os_text, order_flags)
        if res['error']: return {'success': 'false', 'msg': 'Can not order work.'}

        retval['stdout'] = res['stdout']
        retval['stderr'] = res['stderr']
        retval['success'] = 'true'

        return retval

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def upload(self, srcfile=None):

        if 'id' not in cherrypy.session:
            cherrypy.session['id'] = self.generate_session()
            # create session on svcdb
            res = pyrocall(ws_globals['svcdb'].create_opt_session, cherrypy.session['id'])
            if res['error']: return {'success': 'false', 'msg': 'Can not create session.'}

            # set current stage of the session
            res = pyrocall(ws_globals['svcdb'].set_opt_stage, cherrypy.session['id'], self.UPLOAD)
            if res['error']: return {'success': 'false', 'msg': 'Can not set stage.'}
        else:
            # set current stage of the session
            res = pyrocall(ws_globals['svcdb'].set_opt_stage, cherrypy.session['id'], self.UPLOAD)
            if res['error']: return {'success': 'false', 'msg': 'Can not set stage.'}

            # get current stage of the session
            #res = pyrocall(ws_globals['svcdb'].get_opt_stage, cherrypy.session['id'])
            #if res['error']: return {'success': 'false', 'msg': 'Can not get stage.'}

            # check if file upload is valid action on current stage
            #if res.has_key('stage') and res['stage']==self.UPLOAD:
            #    pass
            #else:
            #    return {'success': 'false', 'msg': 'Not compatible stage'}

        retval = {'success': 'true'}

        if srcfile:
            filename = srcfile[0]
            part = srcfile[1]
            
            session_dir = '%s/%s'%(WS_SESSION_HOME, cherrypy.session['id'])
            if not os.path.exists(session_dir):
                os.makedirs(session_dir)
        
            # save file per session
            filepath = '%s/%s'%(session_dir, filename)
            with open(filepath, 'wb') as fd:
                shutil.copyfileobj(part.file, fd)

                # save information on svcdb
                res = pyrocall(ws_globals['svcdb'].save_srcfile, cherrypy.session['id'], filepath)
                if res['error']: return {'success': 'false', 'msg': 'Can not save fileinfo.'}

            # check file type async
            res = pyrocall(ws_globals['xformer'].check_filetype, filepath)
            if res['error']: return {'success': 'false', 'msg': 'Can not check filetype.'}

            # save filetype on svcdb
            res = pyrocall(ws_globals['svcdb'].save_filetype, cherrypy.session['id'], filepath, res['filetype'])
            if res['error']: return {'success': 'false', 'msg': 'Can not save filetype.'}

            # get uploaded files on svcdb
            res = pyrocall(ws_globals['svcdb'].get_uploaded_files, cherrypy.session['id'])
            if res['error']: return {'success': 'false', 'msg': 'Can not save filetype.'}

            ufiles = {}
            for fpath, value in res['uploaded_files'].iteritems():
                ufiles[os.path.basename(fpath)] = value['filetype']
            retval['uploaded_files'] = ufiles

        return retval

    @cherrypy.expose
    def reset(self):
        if 'id' not in cherrypy.session:
            pass
            #return {'success': 'false', 'msg': 'Session does not exist.'}
        else:
            res = ws_globals['svcdb'].reset_opt_session(cherrypy.session['id'])
            if res['error']:
                pass
                #return {'success': 'false', 'msg': 'Can not reset session.'}
            else:
                pass

            print WS_SESSION_HOME, cherrypy.session['id']
            session_dir = '%s/%s'%(WS_SESSION_HOME, cherrypy.session['id'])
            if os.path.exists(session_dir):
                shutil.rmtree(session_dir)

        return self.index()

def start():

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
    ws_globals['xformer'] = Pyro4.Proxy("PYRONAME:act3.xformer")
    ws_globals['svcdb'] = Pyro4.Proxy("PYRONAME:act3.svcdb")
    ws_globals['localcomp'] = Pyro4.Proxy("PYRONAME:act3.localcomp")

    if ws_globals['xformer'] is None or \
        ws_globals['svcdb'] is None or \
        ws_globals['localcomp'] is None:
        raise Exception('Can not connect to Xformer or SvcDB or LocalComp')

    cherrypy.engine.start()
    cherrypy.engine.block()

def stop():
    cherrypy.engine.exit()

if __name__ == '__main__':
    start()
