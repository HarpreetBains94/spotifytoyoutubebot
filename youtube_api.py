from youtube import API

class YoutubeAPI(object):
  api_key = None
  yt = None

  def __init__(self, api_key, *args, **kwargs):
    self.api_key = api_key
    self.set_up_youtube()

  def set_up_youtube(self):
    self.yt = API(client_id='', client_secret='', api_key=self.api_key)
  
  def get_youtube_video(self, search_string):
    video = self.yt.get('search', q=search_string, maxResults=1, type='video', order='relevance')
    return("https://www.youtube.com/watch?v="+video["items"][0]["id"]["videoId"])