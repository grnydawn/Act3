'''Act 3 Service DB Base class'''

class A3FilecheckSvcDB(object):
    __metaclass__ = ABCMeta

    SERVICE_TABLE_NAME = 'filecheck'

    SQL_CREATE_SERVICE_TBL = """CREATE TABLE %s
        (uuid varchar(32),
         password varchar(128),
         email varchar(128),
         phone varchar(128))""" % SERVICE_TABLE_NAME

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
        self.service_tbl_name = A3UserDB.SERVICE_TABLE_NAME
        print ('SVCDB: CONNECTED %s' % db_type)

    def __del__(self):
        print ('SVCDB: CLOSED %s' % self.db_type)

    @abstractmethod
    def addService(self, username, password, email, phone=None):
        pass
