import sys
import os
import glob
import shutil
import signal

SCRIPT_DIR, SCRIPT_NAME = os.path.split(os.path.realpath(__file__))
ACT3_HOME = '%s/..'%SCRIPT_DIR
COMMON_DIR = ACT3_HOME + '/packages'
DOCKER_IMAGE = 'act3_worker:gfortran_4.8.4'

sys.path.insert(0, COMMON_DIR)

from act3_common import runcmd

class A3LocalComp(object):
    def __init__(self):
        print 'LOCALCOMP: READY'

    def __del__(self):
        print 'LOCALCOMP: RELEASED'

    def run(self, session_id, order, src_dir, \
        os_text, order_flags, remove_files=True):
        retval = {'error': True, 'msg': 'Unknown'}
 
        # mkdir build and run subdirectory under session directory
        session_dir = '%s/session/%s'%(SCRIPT_DIR, session_id)
        work_dir = '%s/work'%session_dir
        if not os.path.exists(session_dir): os.makedirs(session_dir)
        if not os.path.exists(work_dir): os.makedirs(work_dir)

        # copy source files into build directory
        for path in glob.iglob('%s/*'%src_dir):
            shutil.copy( path, '%s' % work_dir)
        shutil.copy('%s/script/do.py'%SCRIPT_DIR, session_dir)

        # run docker 
        cmd = 'docker run -t -v %s:/home %s python3 /home/do.py %s %s' % \
            (session_dir, DOCKER_IMAGE, order, order_flags)
        out, err = runcmd(cmd)
        retval['stdout'] = str(out)
        retval['stderr'] = str(err)
        retval['error'] = False
    
        print "STDOUT: ", str(out)
        print "STDERR: ", str(err)

        # analyze the build and run result
        # generate output and return
        
        return retval


localcomp = A3LocalComp()

def signal_handler(signal, frame):
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def main():
    import Pyro4

    daemon = Pyro4.Daemon()
    localcompobj = daemon.register(localcomp)
    ns = Pyro4.locateNS()
    ns.register("act3.localcomp", localcompobj)
    daemon.requestLoop()

if __name__ == "__main__":
    main()
