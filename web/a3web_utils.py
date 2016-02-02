# a3web_utils.py

import sys
import os
import logging
import base64

SCRIPT_DIR, SCRIPT_NAME = os.path.split(os.path.realpath(__file__))
A3_HOME = '%s/..'%SCRIPT_DIR
A3_COMMON = '%s/common'%A3_HOME
sys.path.insert(0, A3_COMMON)

from a3_utils import register_params, get_params, get_logger, common

# web server configuration parameters
web_params_desc = \
    {
        'host-shared': ('/root', 'A folder in the container shared with host', None),
        'json-config': ('web.json', 'A JSON file for Act3 Webserver configuration', None),
        'log-level': ('debug', 'Logging level for  Act3 Webserver',
            {
                'debug': logging.DEBUG,
                'info': logging.INFO,
                'warning': logging.WARNING,
                'error': logging.ERROR,
                'critical': logging.CRITICAL
            }
        ),
        'log-filename': ('web.log', 'A log file for Act3 Webserver', None)
    }

# web server runtime parameters
web_default_runtime = \
{
    'pyro-name-object': None,
    'pyro-sdb-object': None,
    'pyro-kdb-object': None,
    'pyro-udb-object': None,
    'pyro-comp-object': None,
    'pyro-xform-object': None,
    'pyro-web-object': None
}

# web parameter database
web_globals = {}
web_globals['params'] = {}
web_globals['params_desc'] = web_params_desc
web_globals['runtime'] = web_default_runtime
web_globals['common'] = common
web_globals['logger'] =  None

def web_initialize():

    register_params('web', web_globals['params_desc'])

    params = get_params('web')
    web_globals['params'] = params

    logger = get_logger('web', '%s/%s'%(params['host-shared'], params['log-filename']), \
        web_globals['params_desc']['log-level'][2][params['log-level']])
    web_globals['logger'] = logger

    logger.info('Started')

def web_finalize():
    logger().info('Finished')

def get_param(ppath, paramtype='params'):
    try:
        pitem = web_globals[paramtype]
        for pname in ppath.split(':'):
            pitem = pitem[pname]
        return pitem
    except: return None

def set_param(ppath, pvalue, paramtype='params'):
    try:
        pdict = web_globals[paramtype]
        psplit = ppath.split(':')
        nsplit = len(psplit)
        if nsplit==1:
            pdict[ppath] = pvalue
            return pvalue
        elif nsplit>1:
            for pname in psplit[:(nsplit-1)]:
                pdict = pdict[pname]
            if pdict is not None:
                pdict[psplit[-1]] = pvalue
            return pvalue
    except: return None

def get_param_desc(pname):
    try:
        return web_globals['params_desc'][pname]
    except: return None

def logger():
    return web_globals['logger']

def generate_session():
    return base64.b64encode(os.urandom(16), '._')

