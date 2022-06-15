from __future__ import print_function
from distutils.command.install_headers import install_headers
import os.path
from xml.dom.minidom import Document

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class GoogleDocstAPI:
    def __init__(self, SCOPES, CREDENTIAL_PATH = "credentials.json", TOKEN_PATH = "token.json"):
        creds = None;
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(CREDENTIAL_PATH, SCOPES)
                creds = flow.run_local_server(port=0)
                with open(TOKEN_PATH, 'w') as token:
                    token.write(creds.to_json());
        self.service = build('docs', 'v1', credentials=creds)

    