import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class SpotifyAPI(object):
  client_id = None
  client_secret = None
  client_credentials_manager = None
  sp = None

  def __init__(self, client_id, client_secret, *args, **kwargs):
    self.client_id = client_id
    self.client_secret = client_secret
    self.set_up_spotipy()

  def set_up_spotipy(self):
    self.client_credentials_manager = SpotifyClientCredentials(self.client_id, self.client_secret)
    self.sp = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)
  
  def get_track_data(self, url):
    track = self.sp.track(url)
    title = track['name']
    artists_arr = []
    for artist in track['artists']:
      artists_arr.append(artist['name'])
    return {
      'title': title,
      'artists': artists_arr
    }