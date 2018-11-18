from common import auth, responses
import functions
import random
import threading
from flask import Flask, jsonify, request
import common.logger as log
log.setUp()

app = Flask(__name__)

jobs = {}


@auth.authenticate
@functions.storageTokenRequired
def createDownloadJob():
    '''Handler function for starting a download job. \n
    Creates and starts a download job. \n
    Returns the job data immediately and downloads continue in a background thread.
     '''
    try:
        log.start()
        log.info('/download-job'.center(20, '-'))
        functions.setToken(request.headers.get('Token'))
        job_id = random.randint(100, 200)
        job = {'type': 'download', 'complete': False,
               'percentage': 0, 'id': job_id}
        jobs[f'{job_id}'] = job
        download_thread = threading.Thread(
            target=functions.downloadFiles, args=(job,))
        download_thread.start()
        return responses.respondCreated(job)
    except Exception as error:
        return responses.respondInternalServerError(error)


@auth.authenticate
def checkDownloadJobStatus(job_id):
    '''Handler function for checking the status of a download job. \n
    Responds with the data for the specified job
    '''
    try:
        log.start()
        log.info(f'/download-job/{job_id}'.center(20, '-'))
        try:
            job = jobs[job_id]
            return responses.respondWithData(job)
        except KeyError as error:
            log.info(jobs)
            return responses.respondBadRequest(f'Job {job_id} not found')
    except Exception as error:
        log.error('Error:', type(error))
        log.error('Jobs:', jobs)
        return responses.respondInternalServerError(error)


@auth.authenticate
@functions.storageTokenRequired
def createUploadJob():
    '''Handler function for uploading a set of folders. \n
    Creates and starts upload jobs for the folders specified in the
    post requests' json payload. \n
    Returns upload job ids immediately and uploads continue in a background thread
    '''
    try:
        log.start()
        log.info(f'/upload-job'.center(20, '-'))
        classes = validateDataForPostUploadJob(request)
        if not classes == False:
            functions.setToken(request.headers.get('Token'))
            all_folders = functions.getFolderNames('')

            folders_to_upload = [
                name for name in classes if name in all_folders]

            upload_jobs = []
            for folder in folders_to_upload:
                job_id = random.randint(300, 400)
                job = {'type': 'upload', 'complete': False,
                       'percentage': 0, 'id': job_id}
                jobs[f'{job_id}'] = job
                upload_jobs.append(job)
                upload_thread = threading.Thread(name=f'{folder}-upload', target=functions.uploadFiles, args=(
                    f'{folder}', job, f'/{folder}', ))
                upload_thread.start()

            return responses.respondCreated(upload_jobs)
        else:
            return responses.respondBadRequest('Classes not sent')
    except Exception as error:
        return responses.respondInternalServerError(error)


@auth.authenticate
def checkUploadJobStatus(job_id):
    '''Handler for checking the status of an upload. \n
    Returns data on the job with the specified id
    '''
    try:
        log.start()
        log.info(f'/upload-job/{job_id}'.center(20, '-'))
        try:
            job = jobs[job_id]
            return responses.respondWithData(job)
        except KeyError as error:
            return responses.respondBadRequest(f'Job {job_id} not found')
    except Exception as error:
        log.error('Error:', type(error))
        log.error('Jobs:', jobs)
        return responses.respondInternalServerError(error)


def validateDataForPostUploadJob(request):
    '''Validates data for a post upload job route

    Arguments:
        request {flask request object} -- [flask request object]
    '''
    if request.is_json:
        data = request.get_json()
        classes = data['classes']
        if len(classes) >= 1:
            return classes
    return False


app.add_url_rule('/download-job', methods=['POST'],
                 endpoint='download-job', view_func=createDownloadJob)
app.add_url_rule('/download-job/<job_id>', methods=['GET'],
                 endpoint='//download-job/<job_id>', view_func=checkDownloadJobStatus)
app.add_url_rule('/upload-job', methods=['POST'],
                 endpoint='upload-job', view_func=createUploadJob)
app.add_url_rule('/upload-job/<job_id>', methods=['GET'],
                 endpoint='/upload-job/<job_id>', view_func=checkUploadJobStatus)


if __name__ == '__main__':
    '''For test purposes only. When deploying a webserver process such as Gunicorn may be best'''
    app.run(host='127.0.0.1', port=8081, debug=False)
