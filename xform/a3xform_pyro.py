# a3sdb_pyro.py

from a3xform_utils import logger, get_param

class A3SdbPyroIF(object):
    def __init__(self):
        self.db = {}
        self.mgr = get_param('order-mgr')

    def __del__(self):
        pass

    def _get_product(self, order_title, *args, **kwargs):
        retval = {}

        logger().info('%s order is arrived with %s and %s'%(order_title, str(args), str(kwargs)))

        order = self.mgr.make_order(order_title, *args, **kwargs)
        try:
            product = order.execute()
            logger().info('%s order is executed with results of %s'%(order_title, str(product)))
            return product
        except order.GeneralException as e:
            logger().info(str(e))
        except Exception as e:
            logger().info(str(e))

    def check_filetype(self, filepath):
        retval = {'error': False}

        product = self._get_product('filecheck', filepath)
        if product: retval['filetype'] = product.get('filetype', 'Unknown')
        else: retval['error'] = True

        return retval

