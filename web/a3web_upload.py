# a3web_index.py

import os
import shutil
import cherrypy

from a3web_utils import SCRIPT_DIR, generate_session, A3WebSession, get_param, pyrocall, \
    logger

class A3Upload(object):
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
    #def index(self, srcfile=None):
    def index(self, srcfile=None):
        retval = {'success': 'false', 'msg': []}

        # if session does not exist, create one
        if 'id' not in cherrypy.session:
            cherrypy.session['id'] = generate_session()

            # create session on svcdb
            res = pyrocall('sdb', 'create_opt_session', cherrypy.session['id'])
            if res['error']: retval['msg'].append(res['msg'])

        # set current stage of the session
        res = pyrocall('sdb', 'set_opt_stage', cherrypy.session['id'], A3WebSession.UPLOAD)
        if res['error']: retval['msg'].append(res['msg'])

        # if uploaded file exists
        if srcfile:
            filename = srcfile[0]
            part = srcfile[1]

            # create session directory
            session_home = get_param('web-session-dir')
            session_dir = '%s/%s'%(session_home, cherrypy.session['id'])
            if not os.path.exists(session_dir):
                os.makedirs(session_dir)

            # save file per session
            filepath = '%s/%s'%(session_dir, filename)
            with open(filepath, 'wb') as fd:
                shutil.copyfileobj(part.file, fd)

            # save filepath on svcdb
            res = pyrocall('sdb', 'save_srcfile', cherrypy.session['id'], filepath)
            if res['error']: retval['msg'].append(res['msg'])

            # check file type async
            res = pyrocall('xform', 'check_filetype', filepath)
            if res['error']: retval['msg'].append(res['msg'])

            # save filetype on svcdb
            if 'filetype' in res:
                res = pyrocall('sdb', 'save_filetype', cherrypy.session['id'], filepath, res['filetype'])
                if res['error']: retval['msg'].append(res['msg'])

            # get uploaded files on svcdb
            res = pyrocall('sdb', 'get_uploaded_files', cherrypy.session['id'])
            if res['error']: retval['msg'].append(res['msg'])

            if 'uploaded_files' in res:
                ufiles = {}
                for fpath, value in res['uploaded_files'].items():
                    if 'filetype' in value:
                        ufiles[os.path.basename(fpath)] = value['filetype']
                retval['uploaded_files'] = ufiles
                retval['success'] = 'true'
        else:
            retval['msg'].append('Uploaded source file is not correct.')

        return retval
