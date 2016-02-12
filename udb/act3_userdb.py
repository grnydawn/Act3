import sys
import os.path
import signal
import sqlite3
from abc import ABCMeta, abstractmethod

from a3_utils import ACT3_HOME, ACT3_DATA
from a3_utils import setup_remote_call, use_python_3, create_cmdline_args


SCRIPT_NAME = os.path.basename(__file__)
COMMON_DIR = ACT3_HOME + '/common'

sys.path.insert(0, COMMON_DIR)

DB_TYPE_MEMORY = 'memory'
DB_TYPE_SQLITE = 'SQLite'

#
# Only A3UserDBManager should be imported from other package.
# A3UserDBManager will interact with A3UserDB including createUserDB or
# A3UserDB instance will be exposed.
# For example, 
#     from act3_userdb import A3UserDBManager
#     userDb = A3UserDBManager.createUserDB()
#     isValid = userDb.authenticate(username, password):
#
# A3UserDB_Memory and A3UserDB_SQLite should be used internally.
# We can replace the user database with others (MySQL, or commercial databases)
#
    
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

class A3UserDB_Memory(A3UserDB):
    def __init__(self):
        if use_python_3():
            super.__init__('Memory')
        else:
            super(A3UserDB_Memory, self).__init__('Memory')
        self.list = {}

    #def __del__(self):
    #    print 'USERDB: CLOSED - Memory'

    def addUser(self, username, password, email, phone=None):
        #if use_python_3():
        #    super.add_user(username, password, email, phone)
        #else:
        #    super(A3UserDB_Memory, self).addUser(username, password, email, phone)
        self.list[username] = [password, email, phone]
        
    #@
    #@ accepts(int,int)
    #@ returns(float)
    def authenticate(self, username, password):
        result = False
        if self.list.has_key(username):
            result = (password == self.list.get(username)[0])
        return result
    
    def get_all_users(self):
        rows = []
        for user in self.list.keys():
            row = [user]
            for column in self.list.get(user):
                row.append(column)
            rows.append(tuple(row))
        return rows
    
class A3UserDB_SQLite(A3UserDB):
    USER_DB_FILE_NAME = os.path.join(ACT3_DATA, 'user.db')
    
    def __init__(self):
        if use_python_3():
            super.__init__('SQLite')
        else:
            super(A3UserDB_SQLite, self).__init__('SQLite')

        self.initialize()
    
    def __del__(self):
        #self.cursor.close()
        self.conn.close()
        if use_python_3():
            super.__del__('SQLite')
        else:
            super(A3UserDB_SQLite, self).__del__()

    def addUser(self, username, password, email, phone=None):
        sql_string = A3UserDB.SQL_CHECK_USER
        row = self.sql_select_one(sql_string, (username,))
        if None == row or 0 == row[0]:
            sql_string = A3UserDB.SQL_INSERT_USER
            self.sql_insert_replace(sql_string,
                    (username, password, email, phone))
        else:
            sql_string = A3UserDB.SQL_UPDATE_USER
            self.sql_insert_replace(sql_string,
                    (password, email, phone, username))
        self.conn.commit()
        
    def authenticate(self, username, password):
        sql_string = """SELECT COUNT(*) FROM %s
            WHERE username=? AND password=?""" % (
                    self.user_tbl_name)
        row = self.sql_select_one(sql_string, (username, password))
        result = False
        if None != row:
            result = 0 < row[0]
        #print ('record: %r, result: %r' % (row, result))
        return result

    def get_all_users(self):
        rows = self.sql_select(A3UserDB.SQL_SELECT_ALL_USERS)
        return rows
    
    def initialize(self):
        db_file_name = A3UserDB_SQLite.USER_DB_FILE_NAME
        if not os.path.exists(db_file_name):
            dirName = os.path.dirname(db_file_name)
            if not os.path.exists(dirName):
                os.makedirs(dirName)
        self.conn = sqlite3.connect(db_file_name)

        if not self.sql_exist_table(self.user_tbl_name):
            sql_string = A3UserDB.SQL_CREATE_USER_TBL
            self.sql_insert_replace(sql_string)
            self.conn.commit()
        
    def sql_execute(self, sql_string, args = None):
        cursor = self.conn.cursor()
        #print ('args: ',args)
        if None == args:
            cursor.execute(sql_string)
        else:
            cursor.execute(sql_string,args)
        return cursor
        
    def sql_insert_replace(self, sql_string, args=None):
        cursor = self.sql_execute(sql_string, args)
        cursor.close()
        
    def sql_select(self, sql_string, args=None):
        cursor = self.sql_execute(sql_string, args)
        rows = cursor.fetchall()
        cursor.close()
        return rows
        
    def sql_select_one(self, sql_string, args=None):
        cursor = self.sql_execute(sql_string, args)
        row = cursor.fetchone()
        cursor.close()
        return row
        
    def sql_exist_table(self, table_name):
        #result = False
        #sql_string = "SELECT name FROM sqlite_master WHERE type='table' AND name='%s';" % table_name
        sql_string = "SELECT count(*) FROM sqlite_master WHERE type='table' AND name=?;"
        row = self.sql_select_one(sql_string, (table_name,))
        result = (None != row and 1 == row[0])
        return result
    
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
        

def test_db_type(db_type):
    print ('   === test %s ===' % (db_type))
    userDB = A3UserDBManager.createUserDB(db_type)
    user = 'test2'
    password = 'test_password'
    email = 'xxx_test@abc.com'
    userDB.addUser(user,password, email)
    valid = userDB.authenticate(user,password)
    print (' user: %s authenticated: %r' % (user, valid))
    assert (valid == True),"Failed with valid username(%s) and password(%s)" % (user,password)
    password = 'bad_password'
    valid = userDB.authenticate(user,password)
    print (' user: %s authenticated: %r' % (user, valid))
    assert (valid == False),"Succeed with invalid username(%s) and password(%s)" % (user,password)
    
    print ('\n users: %r' % (userDB.get_all_users()))

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


def main(args):
    print ('   ACT3_HOME: %s' % (ACT3_HOME))
    userDB = A3UserDBManager.createUserDB()
    if args.remote_call:
        setup_remote_call("act3.userdb", userDB)
    
    
def main_test(args):
    test_db_type(DB_TYPE_MEMORY)
    print ('\n')
    test_db_type(DB_TYPE_SQLITE)
    print ('\n')

    args2 = create_cmdline_args('user_db', add_more_args)
    obj_without_add_more_args = '%r' % args
    obj_with_add_more_args = '%r' % args2
    
    print('  test_arg: %r' % args2.test_arg)
    assert (-1 == obj_without_add_more_args.find('test_arg')),"SHould not have dummy at args"
    assert (-1 < obj_with_add_more_args.find('test_arg')),"SHould not have dummy at args"

    print ('\n')

def add_more_args(parser):
    parser.add_argument('--test-arg', dest='test_arg', action="store_true", default=False,
        help='Dummy arg for test (Default: disabled)')
    
if __name__ == "__main__":

    args = create_cmdline_args('user_db')
    if args.test:
        main_test(args)
    else:    
        main(args)
    print ('   %s is done' % (SCRIPT_NAME))
