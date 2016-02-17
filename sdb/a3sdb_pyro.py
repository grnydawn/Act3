# a3sdb_pyro.py

class A3SdbPyroIF(object):
    def __init__(self):
        self.db = {}

    def __del__(self):
        pass

    def create_filecheck_order(self, uuid):
        if uuid in self.db:
            return {'error': True, 'msg': 'Filecheck order, %s, already exists.'%uuid}
        else:
            self.db[uuid] = {}
            return {'error': False}

    def remove_filecheck_order(self, uuid):
        if not uuid in self.db:
            return {'error': True, 'msg': 'Filecheck order, %s, does not exist.'%uuid}
        else:
            if 'uploaded_files' in self.db[uuid]:
                del self.db[uuid]['uploaded_files']
            return {'error': False}

    def save_srcfile(self, uuid, fileblob):
        if not uuid in self.db:
            return {'error': True, 'msg': 'Filecheck order, %s, does not exist.'%uuid}
        else:
            if not 'uploaded_files' in self.db[uuid]:
                self.db[uuid]['uploaded_files'] = {}

            # create filecheck order temporary directory
            # save fileblob in the temp directory
            #self.db[uuid]['uploaded_files'][filepath] = {}
            return {'error': False}

    def get_uploaded_files(self, uuid):
        if not uuid in self.db:
            return {'error': True, 'msg': 'Filecheck order, %s, does not exist.'%uuid}
        else:
            if not 'uploaded_files' in self.db[uuid]:
                return {'error': True, 'msg': 'Filecheck order, %s, does not have uploaded file.'%uuid}
            else:
                return {'error': False, 'uploaded_files': self.db[uuid]['uploaded_files']}
