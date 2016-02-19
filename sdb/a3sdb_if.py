# a3sdb_if.py

from a3sdb_utils import get_param, set_param, logger

class SdbInIF(object):
    def __init__(self):
        self.db = {}

    def __del__(self):
        pass

    @staticmethod
    def create_filecheck_order(uuid):
        if uuid in self.db:
            return {'error': True, 'msg': 'Filecheck order, %s, already exists.'%uuid}
        else:
            self.db[uuid] = {}
            return {'error': False}

    @staticmethod
    def remove_filecheck_order(uuid):
        if not uuid in self.db:
            return {'error': True, 'msg': 'Filecheck order, %s, does not exist.'%uuid}
        else:
            if 'uploaded_files' in self.db[uuid]:
                del self.db[uuid]['uploaded_files']
            return {'error': False}

    @staticmethod
    def save_srcfile(uuid, fileblob):
        if not uuid in self.db:
            return {'error': True, 'msg': 'Filecheck order, %s, does not exist.'%uuid}
        else:
            if not 'uploaded_files' in self.db[uuid]:
                self.db[uuid]['uploaded_files'] = {}

            # create filecheck order temporary directory
            # save fileblob in the temp directory
            #self.db[uuid]['uploaded_files'][filepath] = {}
            return {'error': False}

    @staticmethod
    def get_uploaded_files(uuid):
        if not uuid in self.db:
            return {'error': True, 'msg': 'Filecheck order, %s, does not exist.'%uuid}
        else:
            if not 'uploaded_files' in self.db[uuid]:
                return {'error': True, 'msg': 'Filecheck order, %s, does not have uploaded file.'%uuid}
            else:
                return {'error': False, 'uploaded_files': self.db[uuid]['uploaded_files']}
