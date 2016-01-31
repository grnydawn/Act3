# a3_utils.py

import argparse
import logging
import traceback

####################################################
#                  ACT3 Components                 #
####################################################

a3common = \
{
    'services': [ 'a3web' ],
    'a3web':
    {
        'desc': 'Act3 WebServer',
        'pyroname': 'PYRONAME:act3.a3web',
    },
    'xformer':
    {
        'desc': 'Act3 Transformer',
        'pyroname': 'PYRONAME:act3.xformer',
    },

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

def get_a3logger(a3name, filename, level):
    logger = logging.getLogger(a3name.upper())
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

a3params_desc = {}

def register_params(a3name, params_desc):
    a3params_desc[a3name] = params_desc

def get_cmdline_params(a3name):

    parser = argparse.ArgumentParser(description=a3common[a3name]['desc'])
    for pname, (pdefault, pdesc, pmap) in a3params_desc[a3name].items():
        parser.add_argument('--%s'%pname, dest=pname.replace('-', '_'), type=str,
        default=pdefault, help='%s (default: %s)'%(pdesc, pdefault))

    args = parser.parse_args()

    cparams = {}
    for argname, argvalue in vars(args).items():
        cparams[argname.replace('_', '-')] = argvalue

    return cparams

def get_params(a3name):
    params = {}

    # default params
    default_params = {key: value[0] for (key, value) in a3params_desc[a3name].items()}
    params.update(default_params)

    # read command line arguments
    cmdline_params = get_cmdline_params(a3name)
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

