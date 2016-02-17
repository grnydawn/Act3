# a3web_if.py

from a3web_utils import remotecall

class WebIF(object):

    # interface to sdb
    @staticmethod
    def sdb_save_srcfile(uuid, fileblob):
        return remotecall('sdb', 'save_srcfile', uuid, fileblob)

    @staticmethod
    def sdb_create_filecheck_order(uuid):
        return remotecall('sdb', 'create_filecheck_order', uuid)


    # interface to xform
    @staticmethod
    def xform_check_filetype(uuid):
        return remotecall('xform', 'check_filetype', uuid)
