# File Uploader, Downloader service

[![Build Status](https://travis-ci.com/mungujn/downloader-uploader.svg?branch=master)](https://travis-ci.com/mungujn/downloader-uploader)
[![codecov](https://codecov.io/gh/mungujn/downloader-uploader/branch/master/graph/badge.svg)](https://codecov.io/gh/mungujn/downloader-uploader)

## Overview

This service handles the uploading and downloading of files to and from Dropbox. The service exposes 4 endpoints;

1. POST '/download-job'
   This endpoint downloads all files located in a Dropbox folder called 'all' and saves them in the working directory in a folder also called 'all'.
   It returns the data on the newly created download job including a job-id which can be used to check on the completion status of the download job
2. GET '/download-job/job-id'
   This endpoint returns data on the status of a download job
3. POST '/upload-job'
   This endpoint takes a JSON object with an array of classes that were previously classified by the [classifier service](https://github.com/mungujn/classifier-service). It then looks for folders corresponding to the classes then begins uploading them to Dropbox. It returns a JSON object which includes the ID of the upload job
4. GET '/upload-job/job-id'
   This endpoint is used for checking on the status of an upload job

## Configuring Drop box and running the service

- Get a token by following the instructions [here](https://www.dropbox.com/developers/documentation/python)
- Set the token as an environment variable
- Test with pytest, after all tests pass you can start modifying for your own use

This service functions independently, but I built it to work in tandem with the classifier service available [here](https://github.com/mungujn/classifier-service)