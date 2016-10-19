#!/usr/bin/python

import http.client
import httplib2
import os
import random
import progressbar
import time
import re

import googleapiclient.discovery  # build
import googleapiclient.errors  # HTTPError
import googleapiclient.http  # MediaFileUpload
import oauth2client.client  # flow_from_clientsecrets
import oauth2client.file  # Storage
import oauth2client.tools  # argparser, run_flow

# Explicitly tell the underlying HTTP transport library not to retry, since
# we are handling retry logic ourselves.
httplib2.RETRIES = 1

# Maximum number of times to retry before giving up.
MAX_RETRIES = 10

# Always retry when these exceptions are raised.
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error, IOError, http.client.NotConnected,
                        http.client.IncompleteRead, http.client.ImproperConnectionState,
                        http.client.CannotSendRequest, http.client.CannotSendHeader,
                        http.client.ResponseNotReady, http.client.BadStatusLine)

# Always retry when an apiclient.errors.HttpError with one of these status
# codes is raised.
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret. You can acquire an OAuth 2.0 client ID and client secret from
# the {{ Google Cloud Console }} at
# {{ https://cloud.google.com/console }}.
# Please ensure that you have enabled the YouTube Data API for your project.
# For more information about using OAuth2 to access the YouTube Data API, see:
#   https://developers.google.com/youtube/v3/guides/authentication
# For more information about the client_secrets.json file format, see:
#   https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
CLIENT_SECRETS_FILE = "client_secrets.json"

# This OAuth 2.0 access scope allows an application to upload files to the
# authenticated user's YouTube channel, but doesn't allow other types of access.
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

# This variable defines a message to display if the CLIENT_SECRETS_FILE is
# missing.
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the {{ Cloud Console }}
{{ https://cloud.google.com/console }}

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))


def _get_authenticated_service():
    flow = oauth2client.client.flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                                       scope=YOUTUBE_UPLOAD_SCOPE,
                                                       message=MISSING_CLIENT_SECRETS_MESSAGE)

    storage = oauth2client.file.Storage("%s-oauth2.json" % __file__)
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = oauth2client.tools.run_flow(flow, storage)

    return googleapiclient.discovery.build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
                                           http=credentials.authorize(httplib2.Http()))


def _initialize_upload(youtube, filename, body):
    # Call the API's videos.insert method to create and upload the video.
    insert_request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        # The chunksize parameter specifies the size of each chunk of data, in
        # bytes, that will be uploaded at a time. Set a higher value for
        # reliable connections as fewer chunks lead to faster uploads. Set a lower
        # value for better recovery on less reliable connections.
        #
        # Setting "chunksize" equal to -1 in the code below means that the entire
        # file will be uploaded in a single HTTP request. (If the upload fails,
        # it will still be retried where it left off.) This is usually a best
        # practice, but if you're using Python older than 2.6 or if you're
        # running on App Engine, you should set the chunksize to something like
        # 1024 * 1024 (1 megabyte).
        media_body=googleapiclient.http.MediaFileUpload(filename, chunksize=2*1024*1024, resumable=True)
    )

    video_id = _resumable_upload(insert_request, filename)
    return video_id


def _compose_upload_body(filename, title=None, lang=None, description=None):
    tags = [
        'Bhakti Sudhir Goswami (Person)',
        'Bhakti (Religious Practice)',
        'Religion (TV Genre)',
        'Talking',
        'Yoga',
        'Meditation',
        'Guru',
        'India',
        'Temple',
        'Bhakti Yoga',
        'SCSM',
        'Hare Krishna']
    base_filename = os.path.basename(filename)
    if title is None:
        title = base_filename
    if lang is None:
        lang = 'ru' if ((' ru.' in base_filename) or ('_ru.' in base_filename)) else 'en'
    body = dict(
        snippet=dict(
            title=title,
            tags=tags,
            categoryId=27,
            defaultLanguage=lang,
            defaultAudioLanguage=lang
        ),
        status=dict(
            privacyStatus='unlisted',
            publicStatsViewable=False
        )
    )
    if description:
        body['snippet']['description'] = description

    match = re.match('^(\d\d\d\d)-?(\d\d)-?(\d\d)[^0-9]', base_filename)
    if match is not None:
        year, month, day = match.groups()
        recording_date = year + '-' + month + '-' + day + 'T12:45:00.000Z'
    else:
        recording_date = None
    if recording_date is not None:
        body['recordingDetails'] = dict(recordingDate=recording_date)

    return body


# This method implements an exponential backoff strategy to resume a
# failed upload.
def _resumable_upload(insert_request, filename):
    response = None
    error = None
    retry = 0
    print("Uploading file...")
    bar = progressbar.ProgressBar(max_value=os.path.getsize(filename))
    bar.start()
    while response is None:
        try:
            status, response = insert_request.next_chunk()
            if status:
                bar.update(status.resumable_progress)
            if response is not None:
                if 'id' in response:
                    bar.finish()
                    print("Video id '%s' was successfully uploaded." % response['id'])
                    return response['id']
                else:
                    raise Exception("The upload failed with an unexpected response: %s" % response)
        except googleapiclient.errors.HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % (e.resp.status,
                                                                     e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e

        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
                raise Exception("No longer attempting to retry.")

            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)


def upload(filename, title=None, lang=None, description=None):
    youtube = _get_authenticated_service()
    body = _compose_upload_body(filename, title, lang, description)
    return _initialize_upload(youtube, filename, body)


def _main():
    oauth2client.tools.argparser.add_argument("--file", required=True, help="Video file to upload")
    args = oauth2client.tools.argparser.parse_args()
    if not os.path.exists(args.file):
        exit("Please specify a valid file using the --file= parameter.")
    upload(args.file)

if __name__ == '__main__':
    _main()
