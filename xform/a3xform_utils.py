# a3xform_utils.py

import sys
import os
import logging
import base64

SCRIPT_DIR, SCRIPT_NAME = os.path.split(os.path.realpath(__file__))
A3_HOME = '%s/..'%SCRIPT_DIR
A3_COMMON = '%s/common'%A3_HOME
sys.path.insert(0, A3_COMMON)

from a3_utils import common_params, setup_params, create_logger, _get_param, _set_param

# session stage
# ( value, descritpion, value mapping )
user_params_desc = \
    {
        'xform-dir': ('%s/xform'%common_params['host']['shared'], 'A folder in the container for saving xform-related files', None),
        'json-config': ('xform.json', 'A JSON file for Act3 Service DB configuration', None),
        'log-level': ('debug', 'Logging level for  Act3 Service DB',
            {
                'debug': logging.DEBUG,
                'info': logging.INFO,
                'warning': logging.WARNING,
                'error': logging.ERROR,
                'critical': logging.CRITICAL
            }
        ),
        'log-filename': ('xform.log', 'A log file for Act3 Serivce DB', None)
    }

# xform server runtime parameters
runtime_params = \
{
    'pyro-name-object': None,
    'pyro-kdb-object': None,
    'pyro-udb-object': None,
    'pyro-comp-object': None,
    'pyro-sdb-object': None,
    'logger': None,
    'order-mgr': None,
}

# xform parameter database
xform_globals = {}
xform_globals['user_params'] = {}
xform_globals['user_params_desc'] = user_params_desc
xform_globals['runtime_params'] = runtime_params

def xform_initialize():

    params = setup_params('xform', xform_globals['user_params_desc'])
    xform_globals['user_params'] = params

    logger = create_logger('xform', '%s/%s'%(common_params['host']['shared'], \
        params['log-filename']), xform_globals['user_params_desc']['log-level'][2][params['log-level']])
    xform_globals['runtime_params']['logger'] = logger

    # TODO: check if there is dupulication in parameters among runtime, user, and common

    if not os.path.exists(params['xform-dir']):
        os.makedirs(params['xform-dir'])


    logger.info('Started')

def xform_finalize():
    logger().info('Finished')

def get_param(ppath, params='ruc'):
    value = None
    for param in params:
        if param=='r':
            value = _get_param(ppath, xform_globals['runtime_params'])
        elif param=='u':
            value = _get_param(ppath, xform_globals['user_params'])
        elif param=='c':
            value = _get_param(ppath, common_params)
        if value: break
    return value 

def set_param(ppath, pvalue, params='ruc'):
    # TODO: make sure that there is no dupulication in parameters

    value = None
    for param in params:
        if param=='r':
            value = _set_param(ppath, pvalue, xform_globals['runtime_params'])
        elif param=='u':
            value = _set_param(ppath, pvalue, xform_globals['user_params'])
        elif param=='c':
            value = _set_param(ppath, pvalue, common_params)
        if value: break
    return value 

def get_user_param_desc(pname):
    try:
        return xform_globals['user_params_desc'][pname]
    except: return None

def logger():
    return xform_globals['runtime_params']['logger']
