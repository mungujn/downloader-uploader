from functions import downloadFile, uploadFile, getFileNames, getRemoteFileNames, saveFile
import time
import threading
import contextlib

jobs = {}


def newDownloadJob():
    """Creates and starts a download job. Returns immediately and downloads continue in a background thread"""
    job_id = int(time.time())
    job = {'type': 'download', 'complete': False, 'percentage': 0, 'id': job_id}
    jobs[job_id] = job
    upload_thread = threading.Thread(
        target=downloadFiles, args=(job,))
    upload_thread.start()
    return job


def downloadFiles(job):
    """Upload all files in a local folder to dropbox"""
    files = getRemoteFileNames('/all')
    number_of_files = len(files)
    job['number_of_files'] = number_of_files
    job['uploaded'] = 0
    job_id = job['id']
    print(
        f'Job {job_id}: Downloading {number_of_files} files to ../files/all/ folder has started')

    for file in files:
        with timer(job):
            file_data = downloadFile(f'/all/{file}')
            saveFile(file_data, f'../files/all/{file}')

    job['complete'] = True


def newUploadJob(source_folder='../files/all', destination_folder='/all'):
    """Creates and starts an upload job. Returns immediately and uploads continue in a background thread"""
    job_id = int(time.time())
    job = {'type': 'upload', 'complete': False, 'percentage': 0, 'id': job_id}
    jobs[job_id] = job
    upload_thread = threading.Thread(
        target=uploadFiles, args=(source_folder, job, destination_folder))
    upload_thread.start()
    return job


def uploadFiles(local_folder, job, destination_folder):
    """Upload all files in a local folder to dropbox"""
    files = getFileNames(local_folder)
    number_of_files = len(files)
    job['number_of_files'] = number_of_files
    job['uploaded'] = 0
    job_id = job['id']
    print(
        f'Job {job_id}: Uploading {number_of_files} files to {local_folder} folder has started')

    for file in files:
        with timer(job):
            uploadFile(f'{local_folder}/{file}',
                       f'{destination_folder}/{file}')

    job['complete'] = True


@contextlib.contextmanager
def timer(job):
    """Context manager to keep track of a jobs status"""
    try:
        yield
    finally:
        job['uploaded'] += 1
        number_of_files = job['number_of_files']
        uploaded = job['uploaded']
        percentage = int((uploaded/number_of_files)*100)
        job['percentage'] = percentage
        job_id = job['id']
        print(f'Job {job_id} is {percentage} percent complete')


if __name__ == '__main__':
    job = newUploadJob()
    print(job)
