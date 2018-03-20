import requests
import os
import json
import base64

class SpotifyClient():

    spotify_auth_url = "https://accounts.spotify.com/authorize"
    spotify_token_url = "https://accounts.spotify.com/api/token"

    spotify_code = os.environ['SPOTIFY_CODE']
    spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
    spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    spotify_refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN']
    spotify_access_token = os.environ['SPOTIFY_ACCESS_TOKEN']

    def configure_auth_header(self):
        auth_header_param = base64.b64encode(self.spotify_client_id + ":" + self.spotify_client_secret)
        headers = {
            'Authorization': 'Basic % s' % auth_header_param
        }

        return headers

    def get_spotify_auth_url(self):
        query_params = {
            "client_id": os.environ['SPOTIFY_CLIENT_ID'],
            "response_type": "code",
            "redirect_uri": "https://arunvsuresh.wordpress.com/"
        }

        url = self.spotify_auth_url + "?client_id=" + query_params['client_id'] + "&response_type=" + query_params['response_type'] + "&redirect_uri=" + query_params['redirect_uri']

        return url

    def request_access_token(self):
        auth_header_param = base64.b64encode(self.spotify_client_id + ":" + self.spotify_client_secret)
        headers = {
                    'Authorization': 'Basic % s' % auth_header_param
        }

        request_body_params = {
            "grant_type": "authorization_code",
            "code": self.spotify_code,
            "redirect_uri": "https://arunvsuresh.wordpress.com/"
        }

        response = requests.post(self.spotify_token_url, headers=headers, data=request_body_params)
        return response.json()

    def refresh_access_token(self):
        payload = {
            "refresh_token": self.spotify_refresh_token,
            "grant_type": "refresh_token"
        }

        headers = self.configure_auth_header()

        response = requests.post(self.spotify_token_url, headers=headers, data=payload)
        return response.json()['access_token']



