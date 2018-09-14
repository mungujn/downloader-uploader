from flask import jsonify


def respondInternalServerError(error):
    """Returns an object which flask will parse and transform into a 500 response"""
    return (jsonify({'message': 'Internal server error'}), 500)


def respondBadRequest(message):
    """Returns an object which flask will parse and transform into a 400 response"""
    return (jsonify({'message': message}), 400)


def respondUnauthorized(message):
    """Returns an object which flask will parse and transform into a 401 response"""
    return (jsonify({'message': message}), 401)


def respondCreated(data):
    """Returns an object which flask will parse and transform into a 201 response"""
    return (jsonify(data), 201)


def respondOk(data):
    """Returns an object which flask will parse and transform into a 200 response"""
    return (jsonify(data), 200)
