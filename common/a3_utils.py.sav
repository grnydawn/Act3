# a3_utils.py

import os
import argparse
import json
import logging
import inspect
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

common_params = \
{
    'services': [ 'sdb', 'kdb', 'udb', 'comp', 'xform', 'web' ],
    'host': {
        'shared': '/root/shared'
    },
    'name': {
        'desc': 'Act3 Name Server',
        'pyroname': 'Pyro.NameServer',
        'search_interval': 0.1, # in sec
        'search_maxtries': 100,
        'path': '%s/name'%ACT3_HOME,
    },
    'sdb': {
        'desc': 'Act3 Service DB',
        'path': '%s/sdb'%ACT3_HOME,
    },
    'kdb': {
        'desc': 'Act3 Knowledge DB',
        'path': '%s/kdb'%ACT3_HOME,
    },
    'udb': {
        'desc': 'Act3 User DB',
        'path': '%s/udb'%ACT3_HOME,
    },
    'comp': {
        'desc': 'Act3 Computing Resource',
        'path': '%s/comp'%ACT3_HOME,
    },
    'xform': {
        'desc': 'Act3 Transformer',
        'path': '%s/xform'%ACT3_HOME,
    },
    'web': {
        'desc': 'Act3 WebServer',
        'path': '%s/web'%ACT3_HOME,
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

class A3Logger(object):
    def __init__(self, logger):
        self.logger = logger

    def log(self, func, msg, *args, **kwargs):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[2]
        path = '/'.join(os.path.abspath(filename).split('/')[-2:])
        func('%s at %s(%d)'%(msg, path, line_number), *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        self.log(self.logger.debug, msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.log(self.logger.info, msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.log(self.logger.warn, msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.log(self.logger.error, msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.log(self.logger.critical, msg, *args, **kwargs)

    def __getattr__(self, name):
        return getattr(self.logger, name, self.dummy)

def create_logger(svcname, filename, level):
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

    return A3Logger(logger)

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

    parser = argparse.ArgumentParser(description=common_params[svcname]['desc'])
    for pname, (pdefault, pdesc, pmap) in svcdesc.items():
        parser.add_argument('--%s'%pname, dest=pname.replace('-', '_'), type=str,
        default=pdefault, help='%s (default: %s)'%(pdesc, pdefault))

    add_common_args(parser)
    args = parser.parse_args()

    cparams = {}
    for argname, argvalue in vars(args).items():
        cparams[argname.replace('_', '-')] = argvalue

    return cparams

def setup_params(svcname, svcdesc):
    params = {}

    # default params
    default_params = {key: value[0] for (key, value) in svcdesc.items()}
    params.update(default_params)

    # read command line arguments
    cmdline_params = get_cmdline_params(svcname, svcdesc)
    params.update(cmdline_params)

    # params from json file
    try:
        with open('%s/%s'%(common_params['svcname']['path'], params['json-config']), 'r') as f:
            json_params = json.load(f)
            params.update(json_params)
    except: pass

    # overwrite by command line arguments
    params.update(cmdline_params)

    return params

def _get_param(ppath, params):
    try:
        for pname in ppath.split(':'):
            params = params[pname]
        return params
    except: return None

def _set_param(ppath, pvalue, params):
    try:
        psplit = ppath.split(':')
        nsplit = len(psplit)
        if nsplit==1:
            params[ppath] = pvalue
            return pvalue
        elif nsplit>1:
            for pname in psplit[:(nsplit-1)]:
                params = params[pname]
            if params is not None:
                params[psplit[-1]] = pvalue
            return pvalue
    except: return None

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

