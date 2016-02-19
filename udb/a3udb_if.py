# a3udb_if.py


class UdbInIF(object):

    @staticmethod
    def add_user(username, password, email, phone=None):
        userdb = get_param('userdb-obj')
        return userdb.addUser(username, password, email, phone)

