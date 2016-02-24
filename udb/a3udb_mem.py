'''Act 3 User Memory DB'''

from a3udb_base import A3UserDB

DB_TYPE_MEMORY = 'memory'

class A3UserDB_Memory(A3UserDB):
    def __init__(self):
        #super.__init__('Memory')
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

