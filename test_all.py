import functions
import pytest
from flask import json
from service import app
import os
app.testing = True
client = app.test_client()
skip = pytest.mark.skip(reason='fixing other tests')


def test_postDownloadJob():
    """tests the /download-job POST route that adds a new download job
    """
    r = client.post('/download-job')
    data = json.loads(r.data)
    assert data['complete'] == False


def test_getDownloadJob():
    """tests the /download-job/<job-id> GET route that gets the status 
    of a download job
    """
    job_id = 255
    r = client.get(f'/download-job/{job_id}')
    data = json.loads(r.data)
    print(data)
    assert data['message'] == f'Job {job_id} not found'


def test_postUploadJob():
    """tests the /upload-job POST route that adds a new upload job
    """
    r = client.post('/upload-job', json={
        'classes': ['cat', 'dog', 'car']
    })
    data = json.loads(r.data)
    assert len(data) >= 0


def test_getUploadJob():
    """tests the /upload-job/<job_id> GET route that gets upload job
    """
    job_id = 256
    r = client.get(f'/upload-job/{job_id}')
    data = json.loads(r.data)
    print(data)
    assert data['message'] == f'Job {job_id} not found'


def test_getRemoteFileNames():
    """test get remote folder filenames. requires a dropbox folder with 2 files in it
    """
    files = functions.getRemoteFileNames('/test')
    print(files)
    assert len(files) == 2


def test_getFileNames():
    """test getting local filenames
    """
    files = functions.getFileNames('category-1')
    print(files)
    assert len(files) == 4


def test_getFolderNames():
    """test getting names of sub folders in a local folder
    """
    names = functions.getFolderNames('')
    print(names)

    assert len(names) >= 2


def test_uploadFile():
    """test uploading files
    """
    result = functions.uploadFile(
        '', 'test-upload.jpg', '/test/test-upload.jpg')

    assert result == b'test-upload.jpg'


def test_downloadFile():
    """test downloading files
    """
    remote_data = functions.downloadFile('/test/test-download.jpg')

    path = os.path.join('..', 'files', 'test-download.jpg')
    with open(path, 'rb') as f:
        local_data = f.read()

    assert remote_data == local_data


test_downloadFile()


def test_saveFile():
    """test saving files locally
    """
    remote_data = functions.downloadFile('/test/test-download.jpg')
    written = functions.saveFile('', 'test-save.jpg', remote_data)

    assert len(remote_data) == written
