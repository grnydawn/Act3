import sys
import os.path
import signal

SCRIPT_NAME = os.path.basename(__file__)
ACT3_HOME = '%s/..'%os.path.dirname(os.path.realpath(__file__))
COMMON_DIR = ACT3_HOME + '/packages'

sys.path.insert(0, COMMON_DIR)

class A3SvcDB(object):
    def __init__(self):
        self.db = {}
        print 'SVCDB: CONNECTED'

    def __del__(self):
        print 'SVCDB: CLOSED'

    def create_opt_session(self, session_id):
        if self.db.has_key(session_id):
            return {'error': True, 'msg': 'Session %s already exists.'%session_id}
        else:
            self.db[session_id] = {}
            return {'error': False}

    def reset_opt_session(self, session_id):
        if not self.db.has_key(session_id):
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if self.db[session_id].has_key('uploaded_files'):
                del self.db[session_id]['uploaded_files']
            self.db[session_id]['stage'] = 'unknown'
            return {'error': False}

    def set_opt_stage(self, session_id, stage_id):
        if not self.db.has_key(session_id):
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            self.db[session_id]['stage'] = stage_id
            return {'error': False}

    def get_opt_stage(self, session_id):
        if not self.db.has_key(session_id):
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if not self.db[session_id].has_key('stage'):
                return {'error': True, 'msg': 'Session %s does not have stage.'%session_id}
            else:
                return {'error': False, 'stage': self.db[session_id]['stage']}

    def save_srcfile(self, session_id, filepath):
        if not self.db.has_key(session_id):
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if not self.db[session_id].has_key('uploaded_files'):
                self.db[session_id]['uploaded_files'] = {}
            self.db[session_id]['uploaded_files'][filepath] = {}
            return {'error': False}

    def save_filetype(self, session_id, filepath, filetype):
        if not self.db.has_key(session_id):
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if not self.db[session_id].has_key('uploaded_files'):
                return {'error': True, 'msg': 'Session %s does not have uploaded file.'%session_id}
            else:
                if not self.db[session_id]['uploaded_files'].has_key(filepath):
                    return {'error': True, 'msg': 'Session %s does not have %s.'%(session_id, filepath)}
                else:
                    self.db[session_id]['uploaded_files'][filepath]['filetype'] = filetype
                    return {'error': False}

    def get_uploaded_files(self, session_id):
        if not self.db.has_key(session_id):
            return {'error': True, 'msg': 'Session %s does not exist.'%session_id}
        else:
            if not self.db[session_id].has_key('uploaded_files'):
                return {'error': True, 'msg': 'Session %s does not have uploaded file.'%session_id}
            else:
                return {'error': False, 'uploaded_files': self.db[session_id]['uploaded_files']}

svcdb = A3SvcDB()

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    import Pyro4

    daemon = Pyro4.Daemon()
    svcdbobj = daemon.register(svcdb)
    ns = Pyro4.locateNS()
    ns.register("act3.svcdb", svcdbobj)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
