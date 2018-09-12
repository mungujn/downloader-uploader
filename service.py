from functions import downloadFile, uploadFile, getFileNames
import time
import threading
import contextlib
import logging

jobs = {}


def uploadFiles(folder, job_id):
    """Upload all files in a local folder to dropbox"""
    files = getFileNames(folder)
    job = jobs[job_id]
    number_of_files = len(files)
    job['number_of_files'] = number_of_files
    job['uploaded'] = 0
    logging.debug(f'Job {job_id}: Uploading {number_of_files} files to {folder} folder')

    for file in files:
        with timer(job):
            uploadFile(f'../{folder}/{file}', f'/{folder}/{file}')


@contextlib.contextmanager
def timer(job):
    """Context manager to keep track of a jobs status"""
    try:
        yield
    finally:
        job['uploaded'] += 1
        job['status'] = int(job['uploaded']/job['number_of_files'])



if __name__ == '__main__':
    job_id = int(time.time())
    jobs[job_id] = {}
    upload_thread = threading.Thread(target=uploadFiles, args=('All',job_id,))
    upload_thread.start()
