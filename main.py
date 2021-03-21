import os
import discord
from spotify_api import SpotifyAPI
from youtube_api import YoutubeAPI
from keep_alive import keep_alive

client = discord.Client()

@client.event
async def on_ready():
  global spotifyWrapper
  global youtubeWrapper
  spotifyWrapper = SpotifyAPI(os.getenv('SPOTIFY_CLIENT_ID'), os.getenv('SPOTIFY_CLIENT_SECRET'))
  youtubeWrapper = YoutubeAPI(os.getenv('GOOGLE_API_KEY'))
  print('ready')

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.author == os.getenv('STEE'):
    await message.channel.send('You suck')
  content_arr = message.content.split(' ')
  matching_substr = None
  for substr in content_arr:
    if 'https://open.spotify.com/track/' in substr:
      matching_substr = substr
  if matching_substr is None:
    return
  await do_youtube_match(matching_substr, message)

async def do_youtube_match(url, message):
  try:
    track_data = spotifyWrapper.get_track_data(url)
  except:
    await message.channel.send('Invalid Spotify track URL')
    return

  try:
    search_query = track_data['title'] + ' - ' + ' '.join(track_data['artists'])
    video_url = youtubeWrapper.get_youtube_video(search_query)
    await message.channel.send(video_url)
  except:
    await message.channel.send('Unable to find Youtube match')

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))
