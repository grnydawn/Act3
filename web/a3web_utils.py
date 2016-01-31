# a3web_utils.py

import sys
import os
import logging

SCRIPT_DIR, SCRIPT_NAME = os.path.split(os.path.realpath(__file__))
A3_HOME = '%s/..'%SCRIPT_DIR
A3_COMMON = '%s/common'%A3_HOME
sys.path.insert(0, A3_COMMON)

from a3_utils import register_params, get_params, get_a3logger, a3common

# web server configuration parameters
a3web_params_desc = \
    {
        'host-shared': ('/root', 'A folder in the container shared with host', None),
        'json-config': ('a3web.json', 'A JSON file for Act3 Webserver configuration', None),
        'log-level': ('debug', 'Logging level for  Act3 Webserver',
            {
                'debug': logging.DEBUG,
                'info': logging.INFO,
                'warning': logging.WARNING,
                'error': logging.ERROR,
                'critical': logging.CRITICAL
            }
        ),
        'log-filename': ('a3web.log', 'A log file for Act3 Webserver', None)
    }

# web server runtime parameters
a3web_default_runtime = \
{
    'pyro-nameserver-object': None,
    'pyro-xformer-object': None,
}

# a3web parameter database
a3web_globals = {}
a3web_globals['params'] = {}
a3web_globals['params_desc'] = a3web_params_desc
a3web_globals['runtime'] = a3web_default_runtime
a3web_globals['a3common'] = a3common
a3web_globals['logger'] =  None

def a3web_initialize():

    register_params('a3web', a3web_globals['params_desc'])

    params = get_params('a3web')
    a3web_globals['params'] = params

    logger = get_a3logger('a3web', '%s/%s'%(params['host-shared'], params['log-filename']), \
        a3web_globals['params_desc']['log-level'][2][params['log-level']])
    a3web_globals['logger'] = logger

    logger.info('Started')

def a3web_finalize():
    get_logger().info('Finished')

def get_param(pname, paramtype='params'):
    try: return a3web_globals[paramtype][pname]
    except: return None

def set_param(pname, pvalue, paramtype='params'):
    try:
        a3web_globals[paramtype][pname] = pvalue
        return a3web_globals[paramtype][pname]
    except: return None

def get_param_desc(pname):
    try:
        return a3web_globals['params_desc'][pname]
    except: return None

def get_logger():
    return a3web_globals['logger']
