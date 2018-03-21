from unittest import TestCase

import os
import spotify_client


class TestSpotifyClient(TestCase):
    def test_auth_url(self):
        b = spotify_client.SpotifyClient()
        # print b.get_spotify_auth_url()
        # print b.request_access_token()
        # print b.refresh_access_token()
        client_id = spotify_client.SpotifyClient().spotify_client_id

        assert(b.get_spotify_auth_url() == "https://accounts.spotify.com/authorize?client_id={0}&response_type=code&redirect_uri=https://arunvsuresh.wordpress.com/&scope=user-library-read".format(client_id))

    def test_get_user_saved_tracks(self):
        b = spotify_client.SpotifyClient()
        b.spotify_access_token = b.refresh_access_token()['access_token']
        assert(len(b.get_user_saved_tracks()) == b.get_total_num_of_saved_tracks())