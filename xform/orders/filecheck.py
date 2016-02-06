
from a3xform_utils import logger
from a3xform_order import A3Order

class FileCheckOrder(A3Order):
    def __init__(self, filepath):
        self.filepath = filepath
        logger().info('filecheck order is made with %s'%filepath)

        # define a chain of stages
        # preprocesses
        # reader
        # parser
        # analyzer
        # plugin framework
        # plugins
        # ... and cycle back to preprocess

        # cycle -> chain -> stage -> task

    def _execute(self):
        return { 'filetype': 'TBD' }

    def __str__(self):
        return 'Filecheck order'
