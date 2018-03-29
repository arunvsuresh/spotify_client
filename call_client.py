import google_oauth

def add_track_to_sheet():
    google_instance = google_oauth.GoogleOAuth()
    google_instance.google_sheets_access_token = google_instance.refresh_access_token()
    print google_instance.add_saved_spotify_track_to_sheet("1u1d9QY_IEzqugWZ41A960vEULOlL9trPkyZz7GiKOaw")

add_track_to_sheet()

# start_instance_and_add_track_sheet()
