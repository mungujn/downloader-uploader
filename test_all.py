from functions import getFileNames

def test_getFileNames():
    files = getFileNames('../files/category-1')
    assert len(files) == 4