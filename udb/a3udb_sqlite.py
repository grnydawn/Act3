'''Act 3 User Sqlite DB'''

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

