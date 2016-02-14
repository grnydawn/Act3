'''Act 3 User DB Manager'''

class A3UserDBManager(object):
    db_type = None
    userDB  = None

    @staticmethod
    def createUserDB(db_type=None):
        if db_type == A3UserDBManager.db_type:
            userDB = A3UserDBManager.userDB
        else:
            if None == db_type:
                if OPT_USE_SQLITE:
                    db_type = DB_TYPE_SQLITE
                else:
                    db_type = DB_TYPE_MEMORY
            if db_type == DB_TYPE_SQLITE:
                userDB = A3UserDB_SQLite()
            elif db_type == DB_TYPE_MEMORY:
                userDB = A3UserDB_Memory()
            else:
                raise Exception('The type [%s] is not supported' % db_type)
            A3UserDBManager.db_type = db_type
            A3UserDBManager.userDB  = userDB
        return userDB

    def addUser(self, userData):
        pass
