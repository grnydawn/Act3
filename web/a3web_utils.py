# a3web_utils.py

import sys
import os
import logging
import random
import traceback

SCRIPT_DIR, SCRIPT_NAME = os.path.split(os.path.realpath(__file__))
A3_HOME = '%s/..'%SCRIPT_DIR
A3_COMMON = '%s/common'%A3_HOME
sys.path.insert(0, A3_COMMON)

from a3_utils import common_params, setup_params, create_logger, _get_param

# session stage
class A3WebSession(object):
    (UPLOAD, ) = range(1)

# web server configuration parameters
# ( value, descritpion, value mapping )
user_params_desc = \
    {
        'web-session-dir': ('%s/web/sessions'%common_params['host']['shared'], 'A folder in the container for saving session-related files', None),
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
runtime_params = \
{
    'pyro-name-object': None,
    'pyro-sdb-object': None,
    'pyro-kdb-object': None,
    'pyro-udb-object': None,
    'pyro-comp-object': None,
    'pyro-xform-object': None,
    'pyro-web-object': None,
    'logger': None,
}

# web parameter database
web_globals = {}
web_globals['user_params'] = {}
web_globals['user_params_desc'] = user_params_desc
web_globals['runtime_params'] = runtime_params

def web_initialize():

    params = setup_params('web', web_globals['user_params_desc'])
    web_globals['user_params'] = params

    logger = create_logger('web', '%s/%s'%(common_params['host']['shared'], \
        params['log-filename']), web_globals['user_params_desc']['log-level'][2][params['log-level']])
    web_globals['runtime_params']['logger'] = logger

    # TODO: check if there is dupulication in parameters among runtime, user, and common

    if not os.path.exists(params['web-session-dir']):
        os.makedirs(params['web-session-dir'])

    logger.info('Started')

def web_finalize():
    logger().info('Finished')

def get_param(ppath, params='ruc'):
    value = None
    for param in params:
        if param=='r':
            value = _get_param(ppath, web_globals['runtime_params'])
        elif param=='u':
            value = _get_param(ppath, web_globals['user_params'])
        elif param=='c':
            value = _get_param(ppath, common_params)
        if value: break
    return value 

def set_param(ppath, pvalue, params='ruc'):
    # TODO: make sure that there is no dupulication in parameters

    value = None
    for param in params:
        if param=='r':
            value = _set_param(ppath, pvalue, web_globals['runtime_params'])
        elif param=='u':
            value = _set_param(ppath, pvalue, web_globals['user_params'])
        elif param=='c':
            value = _set_param(ppath, pvalue, common_params)
        if value: break
    return value 

def get_user_param_desc(pname):
    try:
        return web_globals['user_params_desc'][pname]
    except: return None

def logger():
    return web_globals['runtime_params']['logger']

def generate_session():
    return 'A3'+'%030x' % random.randrange(16**30)

def pyrocall(destname, funcname, *args, **kwargs):

    try:
        import Pyro4
    except:
        return {'error': True, 'msg': 'Can not import Pyro4 module.'}

    destobj = runtime_params['pyro-%s-object'%destname] 
    if not destobj:
        try:
            destobj = Pyro4.Proxy('PYRONAME:%s'%destname)
        except:
            print('PPPPP;', destname)
            return {'error': True, 'msg': 'Can not get %s Pyro object'%destname}
        if destobj:
            runtime_params['pyro-%s-object'%destname] = destobj

    if destobj:
        try:
            funcobj = getattr(destobj, funcname)
            return funcobj(*args, **kwargs)
        except Exception as e:
            logger().debug(traceback.format_exc())
            logger().debug("".join(Pyro4.util.getPyroTraceback()))
            return {'error': True, 'msg': 'Call to Pyro function, %s.%s, is failed'%(destname, funcname)}
    else:
        return {'error': True, 'msg': 'Pyro object, %s, is None.'%destname}
