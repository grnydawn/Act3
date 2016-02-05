# a3sdb_pyro.py

from a3xform_utils import logger, get_param

class A3SdbPyroIF(object):
    def __init__(self):
        self.db = {}
        self.mgr = get_param('order-mgr')

    def __del__(self):
        pass

    def check_filetype(self, filepath):
        retval = {'error': False}
        retval['filetype'] = 'unknown'

        logger().info('filecheck order is arrived with %s'%filepath)

        order = self.mgr.make_order('filecheck', filepath)
        try:
            product = order.execute()
            logger().info('filecheck order is executed with %s'%product['filetype'])
            retval['filetype'] = product['filetype']
        except order.GeneralException as e:
            logger().info(str(e))
        except Exception as e:
            logger().info(str(e))

        return retval

