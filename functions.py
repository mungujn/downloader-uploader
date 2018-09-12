import os
import dropbox
import logging
from os import listdir
from os.path import isfile, join
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
storage = dropbox.Dropbox(ACCESS_TOKEN)


def getFileNames(folder):
    filenames = []
    for file in listdir(folder):
        if isfile(join(folder, file)):
            filenames.append(join(folder, file))
    return filenames


def downloadFile(path):
    """Download a file"""
    try:
        md, res = storage.files_download(path)
    except dropbox.exceptions.HttpError as error:
        print('*** HTTP error: ', error)
        return None
    data = res.content
    logging.debug(f'{len(data)} bytes; md: {md}')
    return data


def uploadFile(local_path, remote_path):
    """upload a file"""
    mode = (dropbox.files.WriteMode.overwrite)
    with open(local_path, 'rb') as f:
        data = f.read()
    try:
        res = storage.files_upload(data, remote_path, mode)
    except dropbox.exceptions.ApiError as error:
        print('*** API error: ', error)
        return None

    name = res.name.encode('utf8')
    logging.debug(f'uploaded as: {name}')
    return res
