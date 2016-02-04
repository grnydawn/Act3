# a3_utils.py

import os
import argparse
import logging
import inspect
import subprocess

ACT3_HOME = '%s/..'%os.path.dirname(os.path.realpath(__file__))

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

####################################################
#                     Logging                      #
####################################################

class A3Logger(object):
    def __init__(self, logger):
        self.logger = logger

    def log(self, func, msg, *args, **kwargs):
        (frame, filename, line_number,
         function_name, lines, index) = inspect.getouterframes(inspect.currentframe())[3]
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

def get_cmdline_params(svcname, svcdesc):

    parser = argparse.ArgumentParser(description=common_params[svcname]['desc'])
    for pname, (pdefault, pdesc, pmap) in svcdesc.items():
        parser.add_argument('--%s'%pname, dest=pname.replace('-', '_'), type=str,
        default=pdefault, help='%s (default: %s)'%(pdesc, pdefault))

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

####################################################
#                      Shell                       #
####################################################
def runcmd(cmd, input=None):
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, \
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    return proc.communicate(input=input)

