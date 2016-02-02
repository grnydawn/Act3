# a3web_index.py

import cherrypy

from a3_utils import pyrocall
from a3web_utils import SCRIPT_DIR, generate_session, A3WebSession, \
    get_param

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
    def index(self, srcfile=None):
        retval = {'success': 'false', 'msg': 'Unknown'}

        sdb = get_param('pyro-sdb-object')
        if sdb:
            if 'id' not in cherrypy.session:
                cherrypy.session['id'] = generate_session()

                # create session on svcdb
                res = pyrocall(sdb.create_opt_session, cherrypy.session['id'])
                if res['error']: return {'success': 'false', 'msg': 'Can not create session.'}

            # set current stage of the session
            res = pyrocall(sdb.set_opt_stage, cherrypy.session['id'], A3WebSession.UPLOAD)
            if res['error']: return {'success': 'false', 'msg': 'Can not set stage.'}

            if srcfile:
                filename = srcfile[0]
                part = srcfile[1]

                session_home = get_param('web-session-dir')
                session_dir = '%s/%s'%(session_home, cherrypy.session['id'])
                if not os.path.exists(session_dir):
                    os.makedirs(session_dir)

                # save file per session
                filepath = '%s/%s'%(session_dir, filename)
                with open(filepath, 'wb') as fd:
                    shutil.copyfileobj(part.file, fd)

                # save information on svcdb
                res = pyrocall(sdb.save_srcfile, cherrypy.session['id'], filepath)
                if res['error']: return {'success': 'false', 'msg': 'Can not save fileinfo.'}

                xform = get_param('pyro-xform-object')
                if xform:
                    # check file type async
                    res = pyrocall(xform.check_filetype, filepath)
                    if res['error']: return {'success': 'false', 'msg': 'Can not check filetype.'}

                    # save filetype on svcdb
                    res = pyrocall(sdb.save_filetype, cherrypy.session['id'], filepath, res['filetype'])
                    if res['error']: return {'success': 'false', 'msg': 'Can not save filetype.'}

                    # get uploaded files on svcdb
                    res = pyrocall(sdb.get_uploaded_files, cherrypy.session['id'])
                    if res['error']: return {'success': 'false', 'msg': 'Can not save filetype.'}

                    ufiles = {}
                    for fpath, value in res['uploaded_files'].iteritems():
                        ufiles[os.path.basename(fpath)] = value['filetype']
                    retval['uploaded_files'] = ufiles
                    retval['success'] = 'true'
                else:
                    retval['msg'] = 'Xformer is not available.'
            else:
                retval['msg'] = 'Uploaded source file is not correct.'
        else:
            retval['msg'] = 'Service DB is not available.'

        return retval
