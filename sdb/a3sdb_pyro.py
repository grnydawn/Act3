# a3sdb_pyro.py

from a3sdb_if import SdbInIF

class A3SdbPyroIF(object):

    def create_filecheck_order(self, uuid):
        return SdbInIF.create_filecheck_order(uuid)

    def remove_filecheck_order(self, uuid):
        return SdbInIF.remove_filecheck_order(uuid)

    def save_srcfile(self, uuid, fileblob):
        return SdbInIF.save_srcfile(uuid)

    def get_uploaded_files(self, uuid):
        return SdbInIF.get_uploaded_files(uuid)

