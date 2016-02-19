# udb/main.py

import sys
from a3udb_utils import udb_initialize, udb_start, udb_finalize
from a3udb_mgr import A3UserDBManager

def main():

    retval = 0

    # initialize udb
    udb_initialize()

    # create user db
    userdb = A3UserDBManager.createUserDB()

    # start udb
    udb_start(userdb)

    # finalize web
    udb_finalize()

    return retval

if __name__=='__main__':
    sys.exit(main())

