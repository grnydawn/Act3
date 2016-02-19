# a3udb_utils.py

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
    'userdb-obj': None
}

# udb parameter database
udb_globals = {}
udb_globals['user_params'] = {}
udb_globals['user_params_desc'] = user_params_desc
udb_globals['runtime_params'] = runtime_params

def udb_initialize():

    params = setup_params('udb', udb_globals['user_params_desc'])
    udb_globals['user_params'] = params

    logger = create_logger('udb', '%s/%s'%(common_params['host']['shared'], \
        params['log-filename']), udb_globals['user_params_desc']['log-level'][2][params['log-level']])
    udb_globals['runtime_params']['logger'] = logger

    # TODO: check if there is dupulication in parameters among runtime, user, and common

    if not os.path.exists(params['udb-dir']):
        os.makedirs(params['udb-dir'])

    logger.info('Started')

def udb_start(userdb):

    # register user db object
    set_param('userdb-obj', userdb, params='r'):

    # locate Pyro name server
    try:
        import Pyro4
        from a3udb_pyro import Pyro4
        daemon = Pyro4.Daemon()
        udbobj = A3UdbPyroIF()
        udb_uri = daemon.register(udbobj)

        ns = None
        for i in range(get_param('name:search_maxtries')):
            try: ns = Pyro4.locateNS()
            except: pass
            if ns: break
            time.sleep(get_param('name:search_interval'))

        if ns:
            set_param('pyro-name-object', ns)
            ns.register("udb", udb_uri)
            logger().info('udb is registered on a Pyro name server')
            daemon.requestLoop()
            retval = 0
    except ImportError as e:
        logger().warn('udb is not registered on a Pyro name server')
        retval = -1

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
