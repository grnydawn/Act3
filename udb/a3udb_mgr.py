'''Act 3 User DB Manager'''

class A3UserDBMgr(object):
    db_type = None
    userDB  = None

    OPT_USE_SQLITE = True

    @staticmethod
    def createUserDB(db_type=None):
        if None != db_type and db_type == A3UserDBMgr.db_type:
            userDB = A3UserDBMgr.userDB
        else:
            from a3udb_mem    import A3UserDB_Memory, DB_TYPE_MEMORY
            from a3udb_sqlite import A3UserDB_SQLite, DB_TYPE_SQLITE
            
            if None == db_type:
                if A3UserDBMgr.OPT_USE_SQLITE:
                    db_type = DB_TYPE_SQLITE
                else:
                    db_type = DB_TYPE_MEMORY
            if db_type == DB_TYPE_SQLITE:
                userDB = A3UserDB_SQLite()
            elif db_type == DB_TYPE_MEMORY:
                userDB = A3UserDB_Memory()
            else:
                raise Exception('The type [%s] is not supported' % db_type)
            A3UserDBMgr.db_type = db_type
            A3UserDBMgr.userDB  = userDB
        return userDB

    def addUser(self, userData):
        pass
