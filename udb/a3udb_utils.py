# a3udb_utils.py

import sys
import os
import logging
import base64

SCRIPT_DIR, SCRIPT_NAME = os.path.split(__file__)
A3_HOME = os.path.join(SCRIPT_DIR,'..')
A3_COMMON = os.path.join(A3_HOME, 'common')
sys.path.insert(0, A3_COMMON)

from a3_utils import ACT3_HOME
from a3_utils import common_params, setup_params, create_logger, _get_param, _set_param

# session stage
# ( value, descritpion, value mapping )
user_params_desc = \
    {
        'udb-dir': ('%s/udb'%common_params['host']['shared'], 'A folder in the container for saving udb-related files', None),
        'json-config': ('udb.json', 'A JSON file for Act3 User DB configuration', None),
        'log-level': ('debug', 'Logging level for  Act3 User DB',
            {
                'debug': logging.DEBUG,
                'info': logging.INFO,
                'warning': logging.WARNING,
                'error': logging.ERROR,
                'critical': logging.CRITICAL
            }
        ),
        'log-filename': ('udb.log', 'A log file for Act3 User DB', None),
        'debug-level': ('0', 'Set the debug level', {'0':0, '1':1, '2':2,'3':3}),
        'test': ('false', 'Activate the testing part instead of main routines', {'false':False, 'true':True}),
        'test-arg': ('false', 'Dummy arg for test', {'false':False, 'true':True}),
        'remote-call': ('false', 'Activate the remote call (Pyro)', {'false':False, 'true':True})
    }

# udb server runtime parameters
runtime_params = \
{
    'pyro-name-object': None,
    'pyro-kdb-object': None,
    'pyro-sdb-object': None,
    'pyro-comp-object': None,
    'pyro-xform-object': None,
    'logger': None,
}

# udb parameter database
udb_globals = {}
udb_globals['user_params'] = {}
udb_globals['user_params_desc'] = user_params_desc
udb_globals['runtime_params'] = runtime_params

def udb_initialize():
    from a3udb_mgr import A3UserDBMgr
    
    params = setup_params('udb', udb_globals['user_params_desc'])
    udb_globals['user_params'] = params

    shared_dir = common_params['host']['shared']
    if not os.path.exists(shared_dir):
        #env_keys = os.environ.keys()
        if 'ACT3_SHARED' in os.environ.keys():
            shared_dir = os.environ['ACT3_SHARED']
        if not os.path.exists(shared_dir):
            shared_dir = os.path.join(ACT3_HOME, 'shared')
        common_params['host']['shared'] = shared_dir
    logger = create_logger('udb', '%s/%s'%(shared_dir, \
        params['log-filename']), udb_globals['user_params_desc']['log-level'][2][params['log-level']])
    udb_globals['runtime_params']['logger'] = logger

    # TODO: check if there is dupulication in parameters among runtime, user, and common

    if not os.path.exists(params['udb-dir']):
        os.makedirs(params['udb-dir'])

    user_db = A3UserDBMgr.createUserDB()
    udb_globals['user_db'] = user_db
    logger.info('Started')

def udb_finalize():
    logger().info('Finished')

def get_param(ppath, params='ruc'):
    value = None
    for param in params:
        if param=='r':
            value = _get_param(ppath, udb_globals['runtime_params'])
        elif param=='u':
            value = _get_param(ppath, udb_globals['user_params'])
        elif param=='c':
            value = _get_param(ppath, common_params)
        if value: break
    return value 

def set_param(ppath, pvalue, params='ruc'):
    # TODO: make sure that there is no dupulication in parameters

    value = None
    for param in params:
        if param=='r':
            value = _set_param(ppath, pvalue, udb_globals['runtime_params'])
        elif param=='u':
            value = _set_param(ppath, pvalue, udb_globals['user_params'])
        elif param=='c':
            value = _set_param(ppath, pvalue, common_params)
        if value: break
    return value 

def get_user_param_desc(pname):
    try:
        return udb_globals['user_params_desc'][pname]
    except: return None

def logger():
    return udb_globals['runtime_params']['logger']
