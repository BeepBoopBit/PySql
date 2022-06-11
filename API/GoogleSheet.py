from __future__ import print_function
from google.oauth2 import service_account

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os.path


class GoogleSheetAPI:
    def __init__(self, SCOPES, TOKEN_PATH):
        """
        Initializes API Object\n\n
        TOKEN_PATH = `type: string`, the path to your tokens/keys
        """

        self.SERVICE_ACCOUNT_FILE = TOKEN_PATH

        creds = None
        
        if os.path.exists(TOKEN_PATH):
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open(TOKEN_PATH, 'w') as token:
                token.write(creds.to_json())
        self.service = build('sheets', 'v4', credentials=creds)
        pass

    def getSpreadsheetData(self, RANGE_INPUT, SPREADSHEET_ID):
        """
        Returns a dictionary of the spreadsheet.\n\n
        RANGE_INPUT = `type: string`, [more info](https://docs.microsoft.com/en-us/office/vba/excel/concepts/cells-and-ranges/refer-to-cells-and-ranges-by-using-a1-notation) \n\n
        SPREADSHEET_ID = `type: string`
        """

        sheet = self.service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                    range=RANGE_INPUT).execute()
        return result

    def updateSpreadsheetData(self, RANGE_INPUT, SPREADSHEET_ID, data):
        """
        Updates the spreadsheet based on data input.\n\n
        RANGE_INPUT = `type: string`, [more info](https://docs.microsoft.com/en-us/office/vba/excel/concepts/cells-and-ranges/refer-to-cells-and-ranges-by-using-a1-notation) \n\n
        SPREADSHEET_ID = `type: string`\n\n
        data = `type: string`
        """

        sheet = self.service.spreadsheets()
        result = sheet.values().update(
            spreadsheetId=SPREADSHEET_ID,
            range=RANGE_INPUT,
            valueInputOption="USER_ENTERED",
            body={
                "values": data
            }).execute()

        return result

    def addSheet(self, SPREADSHEET_ID, props):
        """
        Adds a Sheet\n\n
        props = `type: object`, refer to [link](https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets#sheetproperties)
        """

        self.__updateSheet(SPREADSHEET_ID, props)

    def deleteSheet(self, SPREADSHEET_ID, SHEET_ID):
        """
        Deletes a Sheet\n
        SPREADSHEET_ID = `type: string`\n\n
        SHEET_ID = `type: string`
        """
        req = {
            "deleteSheet": {
                "sheetId": SHEET_ID
            }
        }

        self.__updateSheet(SPREADSHEET_ID, {"requests": [req]})

    def __updateSheet(self, SPREADSHEET_ID, reqs):
        """
        Creates a sheet, returns the resulting sheet\n
        SPREADSHEET_ID = `type: string`\n\n
        reqs = refer to https://developers.google.com/sheets/api/reference/rest/v4/spreadsheets/sheets\n\n
        """

        sheet = self.service.spreadsheets()
        res = sheet.batchUpdate(
            spreadsheetId=SPREADSHEET_ID, body=reqs).execute()
