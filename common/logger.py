import logging
import common.utils as utils

CONSOLE = True
logger = None
prefix = ''
count = 1

'''logger helper class'''


def setUp():
    '''prepare logger'''
    global logger

    if logger is None:
        logger = logging.getLogger('root')

        logger.setLevel(logging.INFO)

        # create console handler
        ch = logging.StreamHandler()
        eh = logging.StreamHandler()

        # ch.setLevel(logging.INFO)

        eh.setLevel(logging.ERROR)

        # create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        eh.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(ch)
        logger.addHandler(eh)


def start():
    '''starts logging for a request'''
    global prefix
    prefix = utils.getShortUid()


def info(message):
    global count, prefix
    logger.info(f'{prefix} :: {count} :: {message}')
    count += 1


def obj(obj):
    '''log an object to the console'''
    global count, prefix
    logger.info(f'{prefix} :: {count} :: object next')
    count += 1
    print(obj)


def error(message, error=None):
    '''log error message'''
    global count, prefix
    logger.error(f'{prefix} :: {count} :: {message}')
    count += 1
    if error is not None:
        print(type(error))
        print(error)
