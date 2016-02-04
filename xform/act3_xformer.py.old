import sys
import os.path
import signal
from act3_task import TaskFileCheck

SCRIPT_NAME = os.path.basename(__file__)
ACT3_HOME = '%s/..'%os.path.dirname(os.path.realpath(__file__))
COMMON_DIR = ACT3_HOME + '/packages'

sys.path.insert(0, COMMON_DIR)

class A3XFormer(object):
    def __init__(self):
        print 'XFORMER: ACTIVATED'

    def __del__(self):
        print 'XFORMER: DEACTIVATED'

    def check_filetype(self, filepath):
        retval = {'error': False}
        retval['filetype'] = 'unknown'

        task1 = TaskFileCheck(filepath)
        task1_retval = task1.perform_sync()

        if task1_retval['error']:
            pass
        else:
            retval['filetype'] = task1_retval['filetype']
        return retval

xformer = A3XFormer()

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    import Pyro4

    daemon = Pyro4.Daemon()
    xformerobj = daemon.register(xformer)
    ns = Pyro4.locateNS()
    ns.register("act3.xformer", xformerobj)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
