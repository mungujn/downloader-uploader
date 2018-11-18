import os
from dotenv import load_dotenv
load_dotenv()
from functools import wraps
from flask import request
from common import responses
import common.logger as log


def authenticate(f):
    '''Middleware for checking that a correct email address and ticket number is being used'''
    log.start()

    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        service_key = request.headers.get('Authorization', None)

        if service_key is None:
            return responses.respondUnauthorized('No service key supplied')
        else:
            if service_key != os.environ['SERVICE_KEY']:
                return responses.respondUnauthorized('Incorrect service key')
            else:
                return f(*args, **kwargs)
    return decoratedFunction
