from unittest import TestCase

import os
import auth


class TestSpotifyClient(TestCase):
    def test_auth_url(self):
        b = auth.SpotifyAuth()
        print b.get_spotify_auth_url()

    def test_access_token(self):
        b = auth.SpotifyAuth()
        print b.request_access_token()

    def test_refresh_access_token(self):
        b = auth.SpotifyAuth()
        print b.refresh_access_token()

