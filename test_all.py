from functions import getFileNames, downloadFile, uploadFile, saveFile, getRemoteFileNames
import pytest

skip = pytest.mark.skip(reason='no way of currently testing this')


def test_getRemoteFileNames():
    files = getRemoteFileNames('/test')
    print(files)
    assert len(files) == 2


def test_getFileNames():
    files = getFileNames('../files/category-1')
    print(files)
    assert len(files) == 4


def test_uploadFile():
    result = uploadFile('../files/test_upload.jpg', '/Test/test_upload.jpg')

    assert result == b'test_upload.jpg'


def test_downloadFile():
    remote_data = downloadFile('/Test/test_download.jpg')

    with open('../files/test_download.jpg', 'rb') as f:
        local_data = f.read()

    assert remote_data == local_data


def test_saveFile():
    remote_data = downloadFile('/Test/test_download.jpg')
    written = saveFile(remote_data, '../files/test_save.jpg')

    assert len(remote_data) == written


test_getRemoteFileNames()
