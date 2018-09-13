import functions
import random
import threading
import contextlib
from flask import Flask, jsonify, request
from flask_cors import CORS
import responses
app = Flask(__name__)
CORS(app, origins=[])

jobs = {}


@app.route('/download-job', methods=['POST'])
def newDownloadJob():
    """Creates and starts a download job. Returns immediately and downloads continue in a background thread"""
    try:
        job_id = random.randint(100, 200)
        job = {'type': 'download', 'complete': False,
               'percentage': 0, 'id': job_id}
        jobs[f'{job_id}'] = job
        download_thread = threading.Thread(
            target=downloadFiles, args=(job,))
        download_thread.start()
        return responses.respondOk(job)
    except Exception as error:
        print(Exception)
        return responses.respondInternalServerError(error)


@app.route('/download-job/<job_id>', methods=['GET'])
def checkDownloadJobStatus(job_id):
    try:
        try:
            job = jobs[job_id]
            return responses.respondOk(job)
        except KeyError as error:
            return responses.respondBadRequest(f'Job {job_id} not found')
    except Exception as error:
        print('Error:', type(error))
        print('Jobs:', jobs)
        return responses.respondInternalServerError(error)


@app.route('/upload-job', methods=['POST'])
def newUploadJob():
    """
    Creates and starts an upload jobs.
    One job per folder in the working directory except one called 'all'.
    Returns upload job ids immediately and uploads continue in a background thread
    """

    folder_names = functions.getFolderNames('../files/')

    if 'all' in folder_names:
        folder_names.remove('all')

    upload_jobs = []
    for folder in folder_names:
        job_id = random.randint(300, 400)
        job = {'type': 'upload', 'complete': False,
               'percentage': 0, 'id': job_id}
        jobs[job_id] = job
        upload_jobs.append(job)
        upload_thread = threading.Thread(name=f'{folder}-upload', target=uploadFiles, args=(
            f'../files/{folder}', job, f'/{folder}'))
        upload_thread.start()

    return responses.respondCreated(upload_jobs)


@app.route('/upload-job/<job_id>', methods=['GET'])
def checkUploadJobStatus(job_id):
    try:
        try:
            job = jobs[job_id]
            return responses.respondOk(job)
        except KeyError as error:
            return responses.respondBadRequest(f'Job {job_id} not found')
    except Exception as error:
        print('Error:', type(error))
        print('Jobs:', jobs)
        return responses.respondInternalServerError(error)


def downloadFiles(job):
    """Upload all files in a local folder to dropbox"""
    files = functions.getRemoteFileNames('/all')
    number_of_files = len(files)
    job['number_of_files'] = number_of_files
    job['processed'] = 0
    job_id = job['id']
    print(
        f'Job {job_id}: Downloading {number_of_files} files to ../files/all/ folder has started')

    for file in files:
        with timer(job):
            file_data = functions.downloadFile(f'/all/{file}')
            functions.saveFile(file_data, f'../files/all/{file}')

    job['complete'] = True


def uploadFiles(local_folder, job, destination_folder):
    """Upload all files in a local folder to dropbox"""
    files = functions.getFileNames(local_folder)
    number_of_files = len(files)
    job['number_of_files'] = number_of_files
    job['processed'] = 0
    job_id = job['id']
    print(
        f'Job {job_id}: Uploading {number_of_files} files to {local_folder} folder has started')

    for file in files:
        with timer(job):
            functions.uploadFile(f'{local_folder}/{file}',
                                 f'{destination_folder}/{file}')

    job['complete'] = True


@contextlib.contextmanager
def timer(job):
    """Context manager to keep track of a jobs status"""
    try:
        yield
    finally:
        job['processed'] += 1
        number_of_files = job['number_of_files']
        processed = job['processed']
        percentage = int((processed/number_of_files)*100)
        job['percentage'] = percentage
        job_id = job['id']
        print(f'Job {job_id} is {percentage} percent complete')


if __name__ == '__main__':
    """For test purposes only. When deploying a webserver process such as Gunicorn may be best"""
    app.run(host='127.0.0.1', port=8081, debug=True)
