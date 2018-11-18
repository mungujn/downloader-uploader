def getShortUid():
    '''get uuid 4, shortened to first six values'''
    import uuid
    u = str(uuid.uuid4())
    return u[:6]
