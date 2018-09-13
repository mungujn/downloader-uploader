import functions
import random
import threading
import contextlib
from flask import Flask, jsonify, request
import responses
app = Flask(__name__)

jobs = {}


@app.route('/download-job', methods=['POST'])
def createDownloadJob():
    """Handler function for starting a download job. \n
    Creates and starts a download job. \n
    Returns the job data immediately and downloads continue in a background thread.
     """
    try:
        job_id = random.randint(100, 200)
        job = {'type': 'download', 'complete': False,
               'percentage': 0, 'id': job_id}
        jobs[f'{job_id}'] = job
        download_thread = threading.Thread(
            target=downloadFiles, args=(job,))
        download_thread.start()
        return responses.respondCreated(job)
    except Exception as error:
        print(Exception)
        return responses.respondInternalServerError(error)


@app.route('/download-job/<job_id>', methods=['GET'])
def checkDownloadJobStatus(job_id):
    """Handler function for checking the status of a download job. \n
    Responds with the data for the specified job
    """
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
def createUploadJob():
    """Handler function for uploading a set of folders. \n
    Creates and starts upload jobs for the folders specified in the
    post requests' json payload. \n
    Returns upload job ids immediately and uploads continue in a background thread
    """
    try:
        classes = validateDataForPostUploadJob(request)
        if not classes == False:
            all_folders = functions.getFolderNames('')

            folders_to_upload = [
                name for name in classes if name in all_folders]

            upload_jobs = []
            for folder in folders_to_upload:
                job_id = random.randint(300, 400)
                job = {'type': 'upload', 'complete': False,
                       'percentage': 0, 'id': job_id}
                jobs[job_id] = job
                upload_jobs.append(job)
                upload_thread = threading.Thread(name=f'{folder}-upload', target=uploadFiles, args=(
                    f'{folder}', job, f'/{folder}'))
                upload_thread.start()

            return responses.respondCreated(upload_jobs)
        else:
            return responses.respondBadRequest('Classes not sent')
    except Exception as error:
        print(error)
        return responses.respondInternalServerError(error)


@app.route('/upload-job/<job_id>', methods=['GET'])
def checkUploadJobStatus(job_id):
    """Handler for checking the status of an upload. \n
    Returns data on the job with the specified id
    """
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
            functions.saveFile('all', f'{file}', file_data)

    job['complete'] = True
    print(
        f'Job {job_id}: Downloading {number_of_files} files to ../files/all/ folder has completed')


def uploadFiles(local_folder, job, destination_folder):
    """Upload all files in a local_folder to  a destination_folder in dropbox \n
    Job is the job object for the current upload context
    """
    files = functions.getFileNames(local_folder)
    number_of_files = len(files)
    job['number_of_files'] = number_of_files
    job['processed'] = 0
    job_id = job['id']
    print(
        f'Job {job_id}: Uploading {number_of_files} files to {local_folder} folder has started')

    for file in files:
        with timer(job):
            functions.uploadFile(f'{local_folder}', f'{file}',
                                 f'{destination_folder}/{file}')

    job['complete'] = True
    print(
        f'Job {job_id}: Uploading {number_of_files} files to {local_folder} folder has completed')


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


def validateDataForPostUploadJob(request):
    if request.is_json:
        data = request.get_json()
        classes = data['classes']
        if len(classes) >= 1:
            return classes
    return False


if __name__ == '__main__':
    """For test purposes only. When deploying a webserver process such as Gunicorn may be best"""
    app.run(host='127.0.0.1', port=8081, debug=True)
