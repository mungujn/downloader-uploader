import os
import dropbox
import logging
import common.logger as log
from common import responses
from flask import request
import contextlib
from functools import wraps
from os.path import isfile, join, isdir

token = None
storage = None
working_directory = join('..', 'classifier', 'files')


def setToken(new_token):
    global token
    if not new_token == token:
        token = new_token
        setUpDropbox(new_token)


def setUpDropbox(token):
    global storage
    storage = dropbox.Dropbox(token)


def downloadFiles(job):
    '''Upload all files in a local folder to dropbox'''
    try:
        files = getRemoteFileNames('/all')
        number_of_files = len(files)
        job['number_of_files'] = number_of_files
        job['processed'] = 0
        job_id = job['id']
        log.info(
            f'Job {job_id}: Downloading {number_of_files} files to ../files/all/ folder has started')

        for file in files:
            with timer(job):
                file_data = downloadFile(f'/all/{file}')
                saveFile('all', f'{file}', file_data)

        job['complete'] = True
        log.info(
            f'Job {job_id}: Downloading {number_of_files} files to ../files/all/ folder has completed')
    except Exception as error:
        log.info('****error-message****')
        job['complete'] = True
        log.info(
            f'Job {job_id}: Downloading {number_of_files} files to ../files/all/ folder has failed')
        log.info(error)
        log.info('****end-of-error-message****')


def uploadFiles(local_folder, job, destination_folder):
    '''Upload all files in a local_folder to  a destination_folder in dropbox \n
    Job is the job object for the current upload context
    '''
    try:
        files = getFileNames(local_folder)
        number_of_files = len(files)
        job['number_of_files'] = number_of_files
        job['processed'] = 0
        job_id = job['id']
        log.info(
            f'Job {job_id}: Uploading {number_of_files} files to {local_folder} folder has started')

        for file in files:
            with timer(job):
                uploadFile(f'{local_folder}', f'{file}',
                           f'{destination_folder}/{file}')

        job['complete'] = True
        log.info(
            f'Job {job_id}: Uploading {number_of_files} files to {local_folder} folder has completed')
    except Exception as error:
        log.info('****error-message****')
        job['complete'] = True
        log.info(
            f'Job {job_id}: Uploading {number_of_files} files to {local_folder} folder has failed')
        log.info(error)
        log.info('****end-of-error-message****')


@contextlib.contextmanager
def timer(job):
    '''Context manager to keep track of a jobs status'''
    try:
        yield
    finally:
        job['processed'] += 1
        number_of_files = job['number_of_files']
        processed = job['processed']
        percentage = int((processed/number_of_files)*100)
        job['percentage'] = percentage
        # job_id = job['id']
        # log.info(f'Job {job_id} is {percentage} percent complete')


def getRemoteFileNames(remote_folder):
    """Get names of files in a remote_folder"""
    filenames = [file.name for file in storage.files_list_folder(
        remote_folder).entries]
    return filenames


def getFileNames(folder_name):
    """Get names of files in a folder_name"""
    path = join(working_directory, folder_name)
    file_names = []
    for file in os.listdir(path):
        if isfile(join(path, file)):
            file_names.append(file)
    return file_names


def getFolderNames(folder_name):
    """Get names of sub folders in a folder_name"""
    path = join(working_directory, folder_name)
    folder_names = []
    for file in os.listdir(path):
        if isdir(join(path, file)):
            folder_names.append(file)
    return folder_names


def uploadFile(local_folder, file_name, remote_path):
    """upload file in local_folder with file name file_name to remote_path \n
    Returns the uploaded files name
    """
    mode = (dropbox.files.WriteMode.overwrite)
    local_path = join(working_directory, local_folder, file_name)
    with open(local_path, 'rb') as f:
        data = f.read()
    try:
        res = storage.files_upload(data, remote_path, mode)
    except dropbox.exceptions.ApiError as error:
        log.error('*** API error: ', error)
        return None

    name = res.name.encode('utf8')
    logging.debug(f'uploaded as: {name}')
    return name


def downloadFile(remote_path):
    """Download a file from  a remote_path"""
    try:
        md, res = storage.files_download(remote_path)
    except dropbox.exceptions.HttpError as error:
        log.error('*** HTTP error: ', error)
        return None
    data = res.content
    logging.debug(f'{len(data)} bytes; md: {md}')
    return data


def saveFile(folder, file_name, data):
    """Save data as file_name in folder"""
    path = join(working_directory, folder, file_name)
    with open(path, 'w+b') as f:
        written = f.write(data)
    return written


def storageTokenRequired(f):
    '''Middleware for checking that the dropbox token is sent'''
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        token = request.headers.get('Token', None)
        if token is None:
            return responses.respondUnauthorized('No storage token sent')
        return f(*args, **kwargs)

    return decoratedFunction
