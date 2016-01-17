import sys
import os.path
import signal

SCRIPT_NAME = os.path.basename(__file__)
ACT3_HOME = '%s/..'%os.path.dirname(os.path.realpath(__file__))
EXTERNAL_DIR = ACT3_HOME + '/external'

sys.path.insert(0, EXTERNAL_DIR)

class A3UserDB(object):
    def __init__(self):
        print 'USERDB: CONNECTED'

    def __del__(self):
        print 'USERDB: CLOSED'

userdb = A3UserDB()

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    import Pyro4

    daemon = Pyro4.Daemon()
    userdbobj = daemon.register(userdb)
    ns = Pyro4.locateNS()
    ns.register("act3.userdb", userdbobj)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
