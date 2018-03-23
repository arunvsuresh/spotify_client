import requests
import os
import json
from client_id import creds


class GoogleOAuth():
    google_auth_url = creds['web']['auth_uri']
    google_token_url = creds['web']['token_uri']
    google_client_id = creds['web']['client_id']
    google_client_secret = creds['web']['client_secret']
    google_redirect_uri = creds['web']['redirect_uris'][0]
    google_sheets_code = os.environ['GOOGLE_SHEETS_CODE']
    google_sheets_access_token = os.environ['GOOGLE_SHEETS_ACCESS_TOKEN']
    google_sheets_refresh_token = os.environ['GOOGLE_SHEETS_REFRESH_TOKEN']
    google_base_api_url = "https://sheets.googleapis.com/v4/"


    def configure_bearer_auth_header(self):
        headers = {
            'Authorization': 'Bearer % s' % self.google_sheets_access_token
        }

        return headers

    def configure_basic_auth_header(self):
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }

        return headers

    def get_google_auth_url(self):
        query_params = {
            "client_id": self.google_client_id,
            "redirect_uri": self.google_redirect_uri,
            "scope": ['https://www.googleapis.com/auth/spreadsheets'],
            "response_type": "code",
            "access_type": "offline"
        }
        url = self.google_auth_url + "?scope=" + query_params['scope'][0] + "&client_id=" + query_params['client_id'] + "&redirect_uri=" + query_params['redirect_uri'] + "&response_type=" + query_params['response_type'] + "&access_type=" + query_params['access_type']

        return url

    def request_access_token(self):
        headers = self.configure_basic_auth_header()
        request_body_params = {
            "grant_type": "authorization_code",
            "code": self.google_sheets_code,
            "redirect_uri": self.google_redirect_uri,
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret,
        }

        response = requests.post(self.google_token_url, headers=headers, data=request_body_params)
        return response.text

    def refresh_access_token(self):
        headers = self.configure_basic_auth_header()
        payload = {
            "refresh_token": self.google_sheets_refresh_token,
            "grant_type": "refresh_token",
            "client_id": self.google_client_id,
            "client_secret": self.google_client_secret
        }

        response = requests.post(self.google_token_url, headers=headers, data=payload)
        return response.json()['access_token']

    def get_spreadsheet_data(self, id):
        url = self.google_base_api_url + "spreadsheets/" + str(id)
        headers = self.configure_bearer_auth_header()
        response = requests.get(url, headers=headers)
        return response.json()
