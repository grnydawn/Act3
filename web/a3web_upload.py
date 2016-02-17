# a3web_index.py

import os
import shutil
import cherrypy

from a3web_utils import SCRIPT_DIR, A3WebSession, get_param, logger, get_uuid, file2blob
from a3web_if import WebIF

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
    def index(self, uuid=None, srcfile=None):
        retval = {'success': 'false', 'msg': []}

        # if session does not exist, create one
        if uuid is None:
            uuid = get_uuid()

            # create job order entry on svcdb
            res = WebIF.sdb_create_filecheck_order(uuid)
            if res['error']: retval['msg'].append(res['msg'])

        # if uploaded file exists
        if srcfile:
            filename = srcfile[0]
            part = srcfile[1]

            fileblob = file2blob(filename, part.file)

            # send file to svcdb
            res = WebIF.sdb_save_srcfile(uuid, fileblob)
            #res = remotecall('sdb', 'save_srcfile', uuid, fileblob)
            if res['error']: retval['msg'].append(res['msg'])

            # order filecheck
            res = WebIF.xform_check_filetype(uuid)
            #res = remotecall('xform', 'check_filetype', uuid)
            if res['error']: retval['msg'].append(res['msg'])

            # pack response
            if 'filetype' in res:
                retval['filetype'] = {filename: res['filetype']}
                retval['success'] = 'true'
        else:
            retval['msg'].append('Uploaded source file is not correct.')

        return retval
