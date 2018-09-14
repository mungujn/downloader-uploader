# File handler module

## Overview

This service handles the uploading and downloading of files to and from dropbox. The service exposes 4 endpoints;

1. POST '/download-job'
   This endpoint downloads all files located in a dropbox folder called 'all' and saves them in the working directory in a folder also called 'all'.
   It returns the data on the newly created download job including a job-id which can be used to check on the completion status of the download job
2. GET '/download-job/job-id'
   This endpoint returns data on the status of a dowload job
3. POST '/upload-job'
   This endpoint takes a JSON object with an array of classes that were previously classifed by the classifier service. It then looks for folders corresponding to the classes then begins uploading them to dropbox. It returns a JSON object which includes the ID of the upload job
4. GET '/upload-job/job-id'
   This endpoint is used for checking on the status of an upload job