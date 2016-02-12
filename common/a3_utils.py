# a3_utils.py

import os
import argparse
import json
import logging
import subprocess
import traceback

# Do not call os.path.realpath because of using the logical path which maps
# to the real path.
# In program, we are using the logical path, not real path. 
if os.environ.has_key('ACT3_HOME'):
    ACT3_HOME = os.environ.get('ACT3_HOME')
else:
    ACT3_HOME = os.path.join(os.path.dirname(__file__), '..')

if os.environ.has_key('ACT3_DATA'):
    ACT3_DATA = os.environ.get('ACT3_DATA')
else:
    ACT3_DATA = os.path.join(ACT3_HOME, 'data')

####################################################
#                  ACT3 Components                 #
####################################################

common = \
{
    'services': [ 'sdb', 'kdb', 'udb', 'comp', 'xform', 'web' ],
    'name': {
        'desc': 'Act3 Name Server',
        'pyroname': ' PYRO:Pyro.NameServer',
        'search_interval': 0.1, # in sec
        'search_maxtries': 100,
    },
    'sdb': {
        'desc': 'Act3 Service DB',
        'pyroname': 'PYRONAME:act3.sdb',
    },
    'kdb': {
        'desc': 'Act3 Knowledge DB',
        'pyroname': 'PYRONAME:act3.kdb',
    },
    'udb': {
        'desc': 'Act3 User DB',
        'pyroname': 'PYRONAME:act3.udb',
    },
    'comp': {
        'desc': 'Act3 Computing Resource',
        'pyroname': 'PYRONAME:act3.comp',
    },
    'xform': {
        'desc': 'Act3 Transformer',
        'pyroname': 'PYRONAME:act3.xform',
    },
    'web': {
        'desc': 'Act3 WebServer',
        'pyroname': 'PYRONAME:act3.web',
    }
}

####################################################
#                    Exception                     #
####################################################

class A3_Exception(Exception):
    pass

class A3U_Exception(A3_Exception):
    # tell what user did wrong and how to recover
    pass

class A3P_Exception(A3_Exception):
    # tell what A3 did wrong and how to recover
    pass

def use_python_3():
    return False

####################################################
#                     Logging                      #
####################################################

def get_logger(svcname, filename, level):
    logger = logging.getLogger(svcname.upper())
    logger.setLevel(level)

    # create console handler and set level to debug
    fh = logging.FileHandler(filename)
    fh.setLevel(level)
    ch = logging.StreamHandler()
    ch.setLevel(level)

    # create formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # add formatter to ch
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # add ch to logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

####################################################
#                      Params                      #
####################################################

params_desc = {}

def add_common_args(parser):
    parser.add_argument('--log', dest='log', action="store_true", default=False, 
        help='Enabled log message (Default: disabled)')
    parser.add_argument('--log-level', dest='log_level', type=int,
        default=0, help='Set the log level, Default 0')
    parser.add_argument('--debug', dest='debug', action="store_true", default=False,
        help='Enabled debug message (Default: disabled)')
    parser.add_argument('--debug-level', dest='debug_level', type=int,
        default=0, help='Set the debug level, Default 0')
    parser.add_argument('--test', dest='test', action="store_true", default=False,
        help='Activate the testing part instead of main routines (Default: disabled)')
    parser.add_argument('--remote-call', dest='remote_call',
        action="store_true", default=False,
        help='Activate the remote call (Pyro) (Default: disabled)')

def create_cmdline_args(arg_desc, f_add_more_args=None, *args):
    parser = argparse.ArgumentParser(description=arg_desc)
    add_common_args(parser)

    if None != f_add_more_args:
        f_add_more_args(parser, *args)

    args = parser.parse_args()
    return args

   
def register_params(svcname, svcdesc):
    params_desc[svcname] = svcdesc

def get_cmdline_params(svcname):

    parser = argparse.ArgumentParser(description=common[svcname]['desc'])
    for pname, (pdefault, pdesc, pmap) in params_desc[svcname].items():
        parser.add_argument('--%s'%pname, dest=pname.replace('-', '_'), type=str,
        default=pdefault, help='%s (default: %s)'%(pdesc, pdefault))

    add_common_args(parser)
    args = parser.parse_args()

    cparams = {}
    for argname, argvalue in vars(args).items():
        cparams[argname.replace('_', '-')] = argvalue

    return cparams

def get_params(svcname):
    params = {}

    # default params
    default_params = {key: value[0] for (key, value) in params_desc[svcname].items()}
    params.update(default_params)

    # read command line arguments
    cmdline_params = get_cmdline_params(svcname)
    params.update(cmdline_params)

    # params from json file
    try:
        with open('%s/%s'%(params['host-shared'], params['json-config']), 'r') as f:
            json_params = json.load(f)
            params.update(json_params)
    except: pass

    # update from command line arguments
    params.update(cmdline_params)

    return params

####################################################
#                       Pyro                       #
####################################################

def setup_remote_call(name, remote_object):
    method_name = 'setup_remote_call'
    
    try: import Pyro4
    except: raise A3P_Exception('Could not find Pyro module from %s.' % method_name)

    daemon = Pyro4.Daemon()
    #def register(self, obj_or_class, objectId=None, force=False):

    userdbobj = daemon.register(remote_object)
    ns = Pyro4.locateNS()
    #register(self, name, uri, safe=False, metadata=None):
    ns.register(name, userdbobj)
    daemon.requestLoop()
    

def pyrocall(func, *args, **kwargs):
    try: import Pyro4.util
    except: raise A3P_Exception('Could not find Pyro module.')

    try:
        return func(*args, **kwargs)
    except Exception as e:
        tb = traceback.format_exc()
        pyrotb = "".join(Pyro4.util.getPyroTraceback())
        raise A3P_Exception('%s/\n*********** PYRO Exception ***********\n%s'%(tb, pyrotb))

####################################################
#                      Shell                       #
####################################################
def runcmd(cmd, input=None):
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return proc.communicate(input=input)

    try:
        with open('%s/%s'%(SCRIPT_DIR, A3WEB_JSON), 'r') as f:
            json_params = json.load(f)
            params.update(json_params)
    except: pass

