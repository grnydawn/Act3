# sdb/main.py

import sys
import time

from a3sdb_utils import sdb_initialize, sdb_finalize, sdb_start
from a3sdb_mgr import A3ServiceDBManager

def main():

    retval = 0

    # initialize sdb
    sdb_initialize()

    # create service tables
    filecheck = A3ServiceDBManager.createServiceDB('filecheck')

    tables = []
    tables.append(( 'filecheck', filecheck ))

    # start sdb
    sdb_start(tables)

    # finalize web
    sdb_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())

