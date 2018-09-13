from functions import getFileNames, downloadFile, uploadFile, saveFile, getRemoteFileNames, getFolderNames
import pytest
from flask import json
from service import app
app.testing = True
client = app.test_client()
skip = pytest.mark.skip(reason='fixing other tests')


def test_postDownloadJob():
    """test add new download job
    """
    r = client.post('/download-job')
    data = json.loads(r.data)
    assert data['complete'] == False


def test_getDownloadJob():
    """Test get download job
    """
    job_id = 255
    r = client.get(f'/download-job/{job_id}')
    data = json.loads(r.data)
    print(data)
    assert data['message'] == f'Job {job_id} not found'


def test_postUploadJob():
    """test add new upload job
    """
    r = client.post('/upload-job')
    data = json.loads(r.data)
    assert len(data) == 2


def test_getUploadJob():
    """test get upload job
    """
    job_id = 256
    r = client.get(f'/upload-job/{job_id}')
    data = json.loads(r.data)
    print(data)
    assert data['message'] == f'Job {job_id} not found'


def test_getRemoteFileNames():
    """test get remote folder filenames. requires a dropbox folder with 2 files in it
    """
    files = getRemoteFileNames('/test')
    print(files)
    assert len(files) == 2


def test_getFileNames():
    """test getting local filenames
    """
    files = getFileNames('../files/category-1')
    print(files)
    assert len(files) == 4


def test_uploadFile():
    """test uploading files
    """
    result = uploadFile('../files/test_upload.jpg', '/Test/test_upload.jpg')

    assert result == b'test_upload.jpg'


def test_downloadFile():
    """test downloading files
    """
    remote_data = downloadFile('/Test/test_download.jpg')

    with open('../files/test_download.jpg', 'rb') as f:
        local_data = f.read()

    assert remote_data == local_data


def test_saveFile():
    """test saving files locally
    """
    remote_data = downloadFile('/Test/test_download.jpg')
    written = saveFile(remote_data, '../files/test_save.jpg')

    assert len(remote_data) == written


def test_getFolderNames():
    """test getting names of sub folders in a local folder
    """
    names = getFolderNames('../files/')
    print(names)

    assert len(names) == 3
