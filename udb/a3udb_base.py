'''Act 3 User DB Base class'''

class A3UserDB(object):
    __metaclass__ = ABCMeta

    USER_TABLE_NAME = 'user'

    SQL_CREATE_USER_TBL = """CREATE TABLE %s
        (username varchar(128),
         password varchar(128),
         email varchar(128),
         phone varchar(128))""" % USER_TABLE_NAME

    SQL_CHECK_USER = "SELECT COUNT(*) FROM %s WHERE username=?" % (
        USER_TABLE_NAME)
    SQL_INSERT_USER = """INSERT INTO %s
        (username, password, email, phone) VALUES (?,?,?,?)""" % (
        USER_TABLE_NAME)
    SQL_UPDATE_USER = """UPDATE %s SET password=?,email=?,phone=?
        WHERE username=?""" % USER_TABLE_NAME
    SQL_SELECT_ALL_USERS = "SELECT * FROM %s;" % USER_TABLE_NAME

    def __init__(self, db_type=''):
        self.db_type = db_type
        self.user_tbl_name = A3UserDB.USER_TABLE_NAME
        print ('USERDB: CONNECTED %s' % db_type)

    def __del__(self):
        print ('USERDB: CLOSED %s' % self.db_type)

    #@staticmethod
    #def __static_Method(self):
    #    while False:
    #        yield None

    @abstractmethod
    def addUser(self, username, password, email, phone=None):
        pass

    @abstractmethod
    def authenticate(self, username, password):
        pass

    #@abstractmethod
    #def sql_execute(self, sql_string, args = None):
    #    pass

    @abstractmethod
    def get_all_users(self):
        pass

