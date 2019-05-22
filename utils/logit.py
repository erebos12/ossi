import logging
import inspect
import coloredlogs
import os

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.DEBUG)
coloredlogs.install(level='DEBUG')


def log_info(message):
    module, method = get_caller_info()
    logging.info("%s.%s: %s" % (module, method, message))


def log_warning(message):
    module, method = get_caller_info()
    logging.warning("%s.%s: %s" % (module, method, message))


def log_error(message):
    module, method = get_caller_info()
    logging.error("%s.%s: %s" % (module, method, message))


def get_caller_info():
    calling_stack = inspect.stack()[2]
    calling_module = os.path.basename(calling_stack.filename)
    calling_method = calling_stack.function
    return calling_module, calling_method
