# a3_utils.py

import os
import argparse
import logging
import traceback

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

    return logger

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

