import traceback
import logging
import os
from pathlib import Path


ERROR_LOG_FILE = 'log_1.csv'
FILE_LOG_LEVEL = logging.DEBUG
CONSOLE_LOG_LEVEL = logging.ERROR


csv_format = '%(asctime)s,%(thread)d,%(name)s,%(levelno)s,%(levelname)s,%(module)s,%(lineno)d,%(funcName)s,%(message)s'

# create CSV log if none exists
f= open(ERROR_LOG_FILE,"a+")
f.seek(0)
contents = f.read()
if len(contents) == 0:
    # create CSV headers based on csv_format output
    f.write('TIMESTAMP,MILISEC,THREAD ID,NAME,LEVEL NO.,LEVEL NAME,MODULE,LINE NO.,FUNCTION,MESSAGE\n')
f.close()


def get_logger(name):
    """
    method for returning uniform, module-level loggers
    name value should be __name__

    ie. logger = get_logger(__name__)
    """
    # create logger with a given name
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create file handler
    fh = logging.FileHandler(ERROR_LOG_FILE)
    fh.setLevel(FILE_LOG_LEVEL)
    # create console handler with a independent log level
    ch = logging.StreamHandler()
    ch.setLevel(CONSOLE_LOG_LEVEL)
    # create formatter and add it to the handlers
    formatterPlainText = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    formatterCSV = logging.Formatter(csv_format)
    fh.setFormatter(formatterCSV)
    ch.setFormatter(formatterPlainText)
    # add the handlers to the logger
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger

def log_error(logger: logging.Logger, ex):
    logger.exception(ex)
    return ex


def log_app_errors(f):
    """
    logs thrown errors along with stack trace
    use strategically, double error-log entries are common
    """
    def logging_decorator(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            message = 'no message'
            if hasattr(e, 'message'):
                message = e.message
            # rest_framework API exceptions call message 'detail'
            elif hasattr(e, 'detail'):
                message = e.detail

            ex_type = e.__class__.__name__
            stack = traceback.extract_stack()
            func = f.__name__
            error_str = "{}: {} '{}' {}".format(func, ex_type, message, stack)
            module = f.__module__
            logger = get_logger(module)
            logger.error(error_str.replace(",", ".."))
            raise
    return logging_decorator
