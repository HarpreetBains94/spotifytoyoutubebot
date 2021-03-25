import os
import discord
from spotify_api import SpotifyAPI
from youtube_api import YoutubeAPI
from keep_alive import keep_alive
import time

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
  content_arr = message.content.split(' ')
  if content_arr[0] == '!getvid':
    await do_generic_youtube_search(' '.join(content_arr[1:]), message)
    return
  matching_substr_spotify = None
  matching_substr_apple = None
  for substr in content_arr:
    if 'https://open.spotify.com/track/' in substr:
      matching_substr_spotify = substr
    if 'https://music.apple.com/' in substr:
      matching_substr_apple = substr
  if matching_substr_spotify is not None:
    await do_youtube_match_for_spotify(matching_substr_spotify, message)
    return
  if matching_substr_apple is not None:
    """
      Getting the title from the embed in the message for apple links because im not paying
      for an apple developer licence for a dumb discord bot.

      Hopefully this wont have any edge cases/risk conditions
    """
    await message.channel.send('Apple Sucks')
    time.sleep(10)
    channel = message.channel
    new_message = await channel.fetch_message(message.id)
    if new_message.embeds:
      await do_generic_youtube_search(message.embeds[0].title, message)
  

async def do_youtube_match_for_spotify(url, message):
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

async def do_generic_youtube_search(search_query, message):
  try:
    video_url = youtubeWrapper.get_youtube_video(search_query)
    await message.channel.send(video_url)
  except:
    await message.channel.send('Unable to find Youtube match')

keep_alive()
client.run(os.getenv('DISCORD_TOKEN'))
