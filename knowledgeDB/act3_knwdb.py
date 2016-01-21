import sys
import os.path
import signal

SCRIPT_NAME = os.path.basename(__file__)
ACT3_HOME = '%s/..'%os.path.dirname(os.path.realpath(__file__))
COMMON_DIR = ACT3_HOME + '/packages'

sys.path.insert(0, COMMON_DIR)

class A3KnwDB(object):
    def __init__(self):
        print 'KNWDB: CONNECTED'

    def __del__(self):
        print 'KNWDB: CLOSED'

knwdb = A3KnwDB()

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    import Pyro4

    daemon = Pyro4.Daemon()
    knwdbobj = daemon.register(knwdb)
    ns = Pyro4.locateNS()
    ns.register("act3.knwdb", knwdbobj)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
