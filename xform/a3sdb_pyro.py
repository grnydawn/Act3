# a3sdb_pyro.py

class A3SdbPyroIF(object):
    def __init__(self):
        self.db = {}

    def __del__(self):
        pass

    def create_opt_session(self, session_id):
        if session_id in self.db:
            return {'error': True, 'msg': 'Session %s already exists.'%session_id}
        else:
            self.db[session_id] = {}
            return {'error': False}

    def reset_opt_session(self, session_id):
        if not session_id in self.db:
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if 'uploaded_files' in self.db[session_id]:
                del self.db[session_id]['uploaded_files']
            self.db[session_id]['stage'] = 'unknown'
            return {'error': False}

    def set_opt_stage(self, session_id, stage_id):
        if not session_id in self.db:
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            self.db[session_id]['stage'] = stage_id
            return {'error': False}

    def get_opt_stage(self, session_id):
        if not session_id in self.db:
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if not 'stage' in self.db[session_id]:
                return {'error': True, 'msg': 'Session %s does not have stage.'%session_id}
            else:
                return {'error': False, 'stage': self.db[session_id]['stage']}

    def save_srcfile(self, session_id, filepath):
        if not session_id in self.db:
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if not 'uploaded_files' in self.db[session_id]:
                self.db[session_id]['uploaded_files'] = {}
            self.db[session_id]['uploaded_files'][filepath] = {}
            return {'error': False}

    def save_filetype(self, session_id, filepath, filetype):
        if not session_id in self.db:
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if not 'uploaded_files' in self.db[session_id]:
                return {'error': True, 'msg': 'Session %s does not have uploaded file.'%session_id}
            else:
                if not filepath in self.db[session_id]['uploaded_files']:
                    return {'error': True, 'msg': 'Session %s does not have %s.'%(session_id, filepath)}
                else:
                    self.db[session_id]['uploaded_files'][filepath]['filetype'] = filetype
                    return {'error': False}

    def get_uploaded_files(self, session_id):
        if not session_id in self.db:
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if not 'uploaded_files' in self.db[session_id]:
                return {'error': True, 'msg': 'Session %s does not have uploaded file.'%session_id}
            else:
                return {'error': False, 'uploaded_files': self.db[session_id]['uploaded_files']}
