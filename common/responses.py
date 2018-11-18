from flask import jsonify
import common.logger as log


def respondInternalServerError(message='Internal server error', error=None):
    '''Returns an object which flask will parse and transform into a 500 response'''
    log.info('Responding internal server error')
    log.info('*'.center(20, '-'))
    if error is not None:
        log.error(error)
    return (jsonify({
        'code': 500,
        'message': message
    }), 500)


def respondBadRequest(message='Invalid data sent'):
    '''Returns an object which flask will parse and transform into a 400 response'''
    log.info('Responding bad request')
    log.info('*'.center(20, '-'))
    return (jsonify({
        'code': 400,
        'message': message
    }), 400)


def respondUnauthorized(message):
    '''Returns an object which flask will parse and transform into a 401 response'''
    log.info('Responding unauthorized')
    log.info('*'.center(20, '-'))
    return (jsonify({
        'code': 401,
        'message': message
    }), 401)


def respondCreated(data):
    '''Returns an object which flask will parse and transform into a 201 response'''
    log.info('Responding created')
    log.info('*'.center(20, '-'))
    return (jsonify(data), 201)


def respondOk(data):
    '''Returns an object which flask will parse and transform into a 200 response'''
    log.info('Responding OK')
    log.info('*'.center(20, '-'))
    return (jsonify({
        'code': 200,
        'message': data
    }), 200)


def respondWithData(data):
    '''Returns an object which flask will parse and transform into a 200 response
    . This response json will be of the form 
    {
        'code': 200,
        'key_1': 'value_1',
        'key_n': 'value_n'
    }
    '''
    log.info('Responding with data')
    log.info('*'.center(20, '-'))
    t = {'code': 200}
    data = {**t, **data}
    return (jsonify(data), 200)
