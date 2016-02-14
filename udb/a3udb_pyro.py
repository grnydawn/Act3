# a3udb_pyro.py

class A3UdbPyroIF(object):
    def __init__(self):
        self.db = {}

    def __del__(self):
        pass

    def subscribe(self, sessionid, username, password):
        # access User DB to create user profile
        print('UDB: ', sessionid, username, password)

        return { 'error': False }
