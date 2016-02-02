# a3sdb_utils.py

import sys
import os
import logging
import base64

SCRIPT_DIR, SCRIPT_NAME = os.path.split(os.path.realpath(__file__))
A3_HOME = '%s/..'%SCRIPT_DIR
A3_COMMON = '%s/common'%A3_HOME
sys.path.insert(0, A3_COMMON)

from a3sdb_pyro import A3SdbPyroIF
from a3_utils import common_params, setup_params, create_logger, _get_param, _set_param

# session stage
# ( value, descritpion, value mapping )
user_params_desc = \
    {
        'sdb-dir': ('%s/sdb'%common_params['host']['shared'], 'A folder in the container for saving sdb-related files', None),
        'json-config': ('sdb.json', 'A JSON file for Act3 Service DB configuration', None),
        'log-level': ('debug', 'Logging level for  Act3 Service DB',
            {
                'debug': logging.DEBUG,
                'info': logging.INFO,
                'warning': logging.WARNING,
                'error': logging.ERROR,
                'critical': logging.CRITICAL
            }
        ),
        'log-filename': ('sdb.log', 'A log file for Act3 Serivce DB', None)
    }

# sdb server runtime parameters
runtime_params = \
{
    'pyro-name-object': None,
    'pyro-sdb-object': A3SdbPyroIF(),
    'pyro-kdb-object': None,
    'pyro-udb-object': None,
    'pyro-comp-object': None,
    'pyro-xform-object': None,
    'logger': None,
}

# sdb parameter database
sdb_globals = {}
sdb_globals['user_params'] = {}
sdb_globals['user_params_desc'] = user_params_desc
sdb_globals['runtime_params'] = runtime_params

def sdb_initialize():

    params = setup_params('sdb', sdb_globals['user_params_desc'])
    sdb_globals['user_params'] = params

    logger = create_logger('sdb', '%s/%s'%(common_params['host']['shared'], \
        params['log-filename']), sdb_globals['user_params_desc']['log-level'][2][params['log-level']])
    sdb_globals['runtime_params']['logger'] = logger

    # TODO: check if there is dupulication in parameters among runtime, user, and common

    if not os.path.exists(params['sdb-dir']):
        os.makedirs(params['sdb-dir'])

    logger.info('Started')

def sdb_finalize():
    logger().info('Finished')

def get_param(ppath, params='ruc'):
    value = None
    for param in params:
        if param=='r':
            value = _get_param(ppath, sdb_globals['runtime_params'])
        elif param=='u':
            value = _get_param(ppath, sdb_globals['user_params'])
        elif param=='c':
            value = _get_param(ppath, common_params)
        if value: break
    return value 

def set_param(ppath, pvalue, params='ruc'):
    # TODO: make sure that there is no dupulication in parameters

    value = None
    for param in params:
        if param=='r':
            value = _set_param(ppath, pvalue, sdb_globals['runtime_params'])
        elif param=='u':
            value = _set_param(ppath, pvalue, sdb_globals['user_params'])
        elif param=='c':
            value = _set_param(ppath, pvalue, common_params)
        if value: break
    return value 

def get_user_param_desc(pname):
    try:
        return sdb_globals['user_params_desc'][pname]
    except: return None

def logger():
    return sdb_globals['runtime_params']['logger']
