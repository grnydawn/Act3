# a3udb_pyro.py

class A3UdbPyroIF(object):

    def subscribe(self, username, password):
        return UdbInIF.create_user(username, password)

