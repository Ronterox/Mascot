# -*- coding: utf-8 -*-

# Sample Python code for youtube.search.list
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

import os

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from appserve import run_server, request_server

scopes = ["https://www.googleapis.com/auth/youtube.readonly"]

# Disable OAuthlib's HTTPS verification when running locally.
# *DO NOT* leave this option enabled in production.
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

api_service_name = "youtube"
api_version = "v3"
client_secrets_file = "data/client_secret.json"


def find_video(query: str):
    request = youtube.search().list(q=query, part='snippet', type='video')
    response = request.execute()

    firstResult = response['items'][0]
    if firstResult:
        videoId = firstResult['id']['videoId']
        title = firstResult['snippet']['title']
        return videoId, title
    return None, None


def set_credentials():
    global youtube
    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_local_server(port=6969)
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)


def request_video(query: str):
    videoId, title = request_server(query)
    return videoId, title


if __name__ == "__main__":
    set_credentials()
    run_server(find_video)
