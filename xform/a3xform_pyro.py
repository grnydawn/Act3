# a3sdb_pyro.py

from a3xform_utils import logger
from a3xform_task import TaskFileCheck

class A3SdbPyroIF(object):
    def __init__(self):
        self.db = {}

    def __del__(self):
        pass

    def check_filetype(self, filepath):
        retval = {'error': False}
        retval['filetype'] = 'unknown'

        task1 = TaskFileCheck(filepath)
        task1_retval = task1.perform_sync()

        if not task1_retval['error']:
            retval['filetype'] = task1_retval['filetype']

        return retval

