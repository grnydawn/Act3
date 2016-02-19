'''Act 3 Service DB Manager'''

class A3ServiceDBManager(object):
    db_type = None
    serviceDB  = None

    @staticmethod
    def createServiceDB(tablename, db_type=None):
        if db_type == A3ServiceDBManager.db_type:
            userDB = A3ServiceDBManager.serviceDB
        else:
            if None == db_type:
                if OPT_USE_SQLITE:
                    db_type = DB_TYPE_SQLITE
                else:
                    db_type = DB_TYPE_MEMORY
            if db_type == DB_TYPE_SQLITE:
                if tablename == 'filecheck':
                    serviceDB = A3FilecheckDB_SQLite()
            elif db_type == DB_TYPE_MEMORY:
                if tablename == 'filecheck':
                    serviceDB = A3FilecheckDB_Memory()
            else:
                raise Exception('The type [%s] is not supported' % db_type)
            A3ServiceDBManager.db_type = db_type
            A3ServiceDBManager.serviceDB  = serviceDB
        return serviceDB
