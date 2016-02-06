'''Order Handling Routines'''

import sys
from a3xform_utils import SCRIPT_DIR

sys.path.append('%s/orders'%SCRIPT_DIR)

from filecheck import FileCheckOrder

class A3OrderMgr(object):

    def make_order(self, order_title, *args, **kwargs):
        if order_title=='filecheck':
            return FileCheckOrder(*args, **kwargs)
        else:
            raise Exception('%s order is not supported.'%order_title)

