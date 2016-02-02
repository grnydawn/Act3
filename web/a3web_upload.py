# a3web_index.py

import cherrypy

from a3web_utils import SCRIPT_DIR, generate_session, pyrocall, A3WebSession

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
    def index(self, srcfile=None):
        sdb = get_param('pyro-sdb-object', paramtype='runtime')
        if sdb:
            if 'id' not in cherrypy.session:
                cherrypy.session['id'] = generate_session()
                # create session on svcdb
                res = pyrocall(sdb.create_opt_session, cherrypy.session['id'])
                if res['error']: return {'success': 'false', 'msg': 'Can not create session.'}

                # set current stage of the session
                res = pyrocall(sdb.set_opt_stage, cherrypy.session['id'], A3WebSession.UPLOAD)
                if res['error']: return {'success': 'false', 'msg': 'Can not set stage.'}
            else:
                # set current stage of the session
                res = pyrocall(sdb.set_opt_stage, cherrypy.session['id'], A3WebSession.UPLOAD)
                if res['error']: return {'success': 'false', 'msg': 'Can not set stage.'}
        else:
                if res['error']: return {'success': 'false', 'msg': 'Service DB is not available.'}

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

