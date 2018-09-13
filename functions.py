import os
import dropbox
import logging
from os.path import isfile, join, isdir
from dotenv import load_dotenv
load_dotenv()

ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
storage = dropbox.Dropbox(ACCESS_TOKEN)
working_directory = join('..', 'files')


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
        print('*** API error: ', error)
        return None

    name = res.name.encode('utf8')
    logging.debug(f'uploaded as: {name}')
    return name


def downloadFile(remote_path):
    """Download a file from  a remote_path"""
    try:
        md, res = storage.files_download(remote_path)
    except dropbox.exceptions.HttpError as error:
        print('*** HTTP error: ', error)
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
