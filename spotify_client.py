import requests
import os
import json
import base64
import itertools


class SpotifyClient():

    spotify_auth_url = "https://accounts.spotify.com/authorize"
    spotify_token_url = "https://accounts.spotify.com/api/token"
    spotify_api_base_url = "https://api.spotify.com/v1"

    spotify_code = os.environ['SPOTIFY_CODE']
    spotify_client_id = os.environ['SPOTIFY_CLIENT_ID']
    spotify_client_secret = os.environ['SPOTIFY_CLIENT_SECRET']
    spotify_refresh_token = os.environ['SPOTIFY_REFRESH_TOKEN']
    spotify_access_token = os.environ['SPOTIFY_ACCESS_TOKEN']

    def configure_bearer_auth_header(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer % s' % self.spotify_access_token
        }

        return headers

    def configure_basic_auth_header(self):
        auth_header_param = base64.b64encode(self.spotify_client_id + ":" + self.spotify_client_secret)
        headers = {
            'Authorization': 'Basic % s' % auth_header_param
        }

        return headers

    def get_spotify_auth_url(self):
        query_params = {
            "client_id": os.environ['SPOTIFY_CLIENT_ID'],
            "response_type": "code",
            "redirect_uri": "https://arunvsuresh.wordpress.com/",
            "scope": "user-library-read"
        }

        url = self.spotify_auth_url + "?client_id=" + query_params['client_id'] + "&response_type=" + query_params['response_type'] + "&redirect_uri=" + query_params['redirect_uri'] + "&scope=" + query_params['scope']
        return url

    def request_access_token(self):
        headers = self.configure_basic_auth_header()
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

        headers = self.configure_basic_auth_header()

        response = requests.post(self.spotify_token_url, headers=headers, data=payload)
        return response.json()['access_token']

    def get_total_num_of_saved_tracks(self):
        user_track_url = self.spotify_api_base_url + "/me/tracks/"
        headers = self.configure_bearer_auth_header()
        response = requests.get(user_track_url, headers=headers)
        return response.json()['total']

    def get_user_saved_tracks(self):
        track_per_page_limit = 50
        user_track_url = self.spotify_api_base_url + "/me/tracks/?offset=0&limit={0}".format(track_per_page_limit)
        headers = self.configure_bearer_auth_header()
        response = requests.get(user_track_url, headers=headers)
        end = int(round(int(response.json()['total']) / track_per_page_limit))
        saved_tracks = []
        saved_tracks.append(response.json()['items'])
        for i in range(0, end):
            # offset is multiple of 50
            offset = (i + 1) * track_per_page_limit
            # use offset to get every page
            url = self.spotify_api_base_url + "/me/tracks/?offset={0}&limit={1}".format(offset, track_per_page_limit)
            response = requests.get(url, headers=headers)
            saved_tracks.append(response.json()['items'])

        saved_tracks = list(itertools.chain.from_iterable(saved_tracks))
        return saved_tracks

    def get_last_saved_track(self):
        user_track_url = self.spotify_api_base_url + "/me/tracks/"
        headers = self.configure_bearer_auth_header()
        response = requests.get(user_track_url, headers=headers)
        return response.json()['items'][0]['track']['name']
