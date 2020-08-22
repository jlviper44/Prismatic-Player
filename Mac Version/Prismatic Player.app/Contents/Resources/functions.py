import tkinter as tk
from PIL import ImageTk, Image, ImageStat, ImageFilter
from tkinter import StringVar, IntVar
import os
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import operator
import datetime
import numpy as np

class song:
  def __init__(this, spotify, currentSong):
    this.spotify = spotify
    this.currentSong = currentSong
    if(currentSong == None):
      this.albumArtwork = ''
      this.albumArtworkSmall = ''
      this.name = ''
      this.artist = ''
      this.currentTime = ''
      this.totalTime = ''
      this.isPlaying = 'none'
    elif(currentSong.get('currently_playing_type') == 'ad' or currentSong.get('currently_playing_type') == 'episode'):
      this.albumArtwork = ''
      this.albumArtworkSmall = ''
      this.name = ' '
      this.artist = ''
      this.currentTime = ''
      this.totalTime = ''
      this.isPlaying = 'ad'
    else:
      this.albumArtwork = currentSong.get('item')['album']['images'][0]['url']
      this.albumArtworkSmall = currentSong.get('item')['album']['images'][2]['url']
      this.name = currentSong.get('item')['name']
      if(len(this.name) > 35):
        position = this.name.find('(')
        if(position != -1):
          this.name = this.name[0:position]
        else:
          position = this.name.find('-')
          if(position != -1):
            this.name = this.name[0:position - 1]
          else:
            this.name = this.name[0:32]+'...'
      this.artist = currentSong.get('item')['artists'][0]['name']
      this.currentTime = currentSong.get('progress_ms')
      this.totalTime = currentSong.get('item')['duration_ms']
      this.isPlaying = True  
  def getAlbumArtwork(this, scale, frame):
    if(this.isPlaying == True):
      response = requests.get(this.albumArtwork)
      img_data = response.content
      image = Image.open(BytesIO(img_data))
      image = image.resize((int(600 * scale), int(600 * scale)), Image.ANTIALIAS)
      img = ImageTk.PhotoImage(image)
      return img
    else:
      if(int(600 * scale) >= 1000):
        animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_1000.npy', allow_pickle=True)
      elif(int(600 * scale) >= 800):
        animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_800.npy', allow_pickle=True)
      elif(int(600 * scale) >= 600):
        animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_600.npy', allow_pickle=True)
      elif(int(600 * scale) >= 400):
        animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_400.npy', allow_pickle=True)
      else:
        animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_200.npy', allow_pickle=True)
      # image = Image.open(filename)
        # image = image.resize((int(200 * scale), int(200 * scale)), Image.ANTIALIAS)
      # img = ImageTk.PhotoImage(image)
      img = tk.PhotoImage(data = animationLoadingJpg[0])
      return img
  def getRgb(this):
    if(this.isPlaying == True):
      response = requests.get(this.albumArtworkSmall)
      img_data = response.content
      image = Image.open(BytesIO(img_data))
      colorsMain = {}
      colorsSecondary = {}
      # for x in range(8):
      #   currentColor = Image.open(BytesIO(img_data)).getpixel((8*x,4))
      #   if(currentColor in colorsMain):
      #     colorsMain[currentColor] += 1
      #   else:
      #     colorsMain[currentColor] = 1
      for x in range(8):
        currentColor1 = Image.open(BytesIO(img_data)).getpixel((8 * x,4))
        if(currentColor1 in colorsMain):
          colorsMain[currentColor1] += 1
        else:
          colorsMain[currentColor1] = 1
        for y in range(8):
          # currentColor = Image.open(BytesIO(img_data)).getpixel((16*x,16*y-1))
          currentColor = Image.open(BytesIO(img_data)).getpixel((28 + x,28 + y))
          if(currentColor in colorsSecondary):
            colorsSecondary[currentColor] += 1
          else:
            colorsSecondary[currentColor] = 1
      sort_colors =  sorted(colorsSecondary.items(), key=lambda x: x[1], reverse=True)
      try:
        # dominantColor = max(colorsMain.items(), key=operator.itemgetter(1))[0]
        # secondaryColor = max(colorsSecondary, key=lambda x: x[1])
        # thirdColor = max(colorsSecondary, key=lambda x: x[2])
        
        dominantColor = max(colorsMain.items(), key=operator.itemgetter(1))[0]
        secondaryColor = sort_colors[1][0]
        thirdColor = sort_colors[2][0]
        # print(sort_colors[1][0])
        # print(sort_colors)
        # print(secondaryColor)
        i=2
        if((dominantColor[0] - 75 <= secondaryColor[0] <= dominantColor[0] + 75) and
           (dominantColor[1] - 75 <= secondaryColor[1] <= dominantColor[1] + 75) and
           (dominantColor[2] - 75 <= secondaryColor[2] <= dominantColor[2] + 75)):
          difference = 765 - secondaryColor[0] - secondaryColor[1] - secondaryColor[2]
          if(difference <= 380):
            secondaryColor = (0,0,0)
          else:
            secondaryColor = (255,255,255)
        
        if((dominantColor[0] - 50 <= thirdColor[0] <= dominantColor[0] + 50) and
           (dominantColor[1] - 50 <= thirdColor[1] <= dominantColor[1] + 50) and
           (dominantColor[2] - 50 <= thirdColor[2] <= dominantColor[2] + 50)):
          while(True):
            thirdColor = sort_colors[i][0]
            if(i > 4):
              thirdColor = secondaryColor
              break
            elif((dominantColor[0] - 50 <= thirdColor[0] <= dominantColor[0] + 50) and
                 (dominantColor[1] - 50 <= thirdColor[1] <= dominantColor[1] + 50) and
                 (dominantColor[2] - 50 <= thirdColor[2] <= dominantColor[2] + 50)):
              i+=1
            else:
              break
      except:
        #comment this out to reduce lag
        try:
          dominantColor = max(colorsMain.items(), key=operator.itemgetter(1))[0]
          try:
            if(dominantColor[0] >= 125):
              dominantColor = (255,255,255)
              secondaryColor = (0,0,0)
              thirdColor = (0,0,0)
            else:
              dominantColor = (0,0,0)
              secondaryColor = (255,255,255)
              thirdColor = (255,255,255)
          except:
            if(dominantColor >= 125):
              dominantColor = (255,255,255)
              secondaryColor = (0,0,0)
              thirdColor = (0,0,0)
            else:
              dominantColor = (0,0,0)
              secondaryColor = (255,255,255)
              thirdColor = (255,255,255)
        except:
          dominantColor = (0,0,0)
          secondaryColor = (255,255,255)
          thirdColor = (255,255,255)

      dominantColorHex = '#%02x%02x%02x' % dominantColor
      secondaryColorHex = '#%02x%02x%02x' % secondaryColor
      thirdColorHex = '#%02x%02x%02x' % thirdColor
      return [dominantColorHex, secondaryColorHex,thirdColorHex]
    else:
      if(this.isPlaying == 'none'):
        return ['black','white','black']
      else:
        return ['black','black','black']
  def getCurrentTime(this):
    if(this.isPlaying == True):
      currentTime = abs(int(this.currentTime/1000))
      currentTimeText = ""
      if(((currentTime % 60) < 10) and (currentTime/60 < 1)):
        currentTimeText = "0:0" + str(currentTime % 60)
      elif(((currentTime % 60) < 60) and (currentTime/60 < 1)):
        currentTimeText = "0:" + str(currentTime % 60)
      elif(((currentTime % 60) < 10) and (currentTime/60 >= 1)):
        currentTimeText = str(int(currentTime / 60)) + ":0" +str(currentTime % 60)
      else:
        currentTimeText = str(int(currentTime / 60)) + ":" +str(currentTime % 60)
      time = currentTimeText
    else:
      time = ''
    return time
  def getTotalTime(this):
    if(this.isPlaying == True):
      totalTime = abs(int(this.totalTime/1000))
      totalTimeText = ""
      if(((totalTime % 60) < 10) and (totalTime/60 < 1)):
        totalTimeText = "0:0" + str(totalTime % 60)
      elif(((totalTime % 60) < 60) and (totalTime/60 < 1)):
        totalTimeText = "0:" + str(totalTime % 60)
      elif(((totalTime % 60) < 10) and (totalTime/60 >= 1)):
        totalTimeText = str(int(totalTime / 60)) + ":0" +str(totalTime % 60)
      else:
        totalTimeText = str(int(totalTime / 60)) + ":" +str(totalTime % 60)
      time = totalTimeText
    else:
      time = ''
    return time
  def getTimeBar(this):
    if(this.isPlaying == True):
      return this.currentTime / this.totalTime
    else:
      return 0
  def getPlaybackState(this):
    if(this.isPlaying == True):
      playbackInfo = this.currentSong
      return playbackInfo.get('is_playing')
    else:
      return False
  def getPlaybackSource(this,orientation):
    if(this.isPlaying == True):
      if(orientation == "horizontal"):
        try:
          playbackType = this.currentSong.get('context')['type']
          if(playbackType == "playlist"):
            uri = this.currentSong.get('context')['uri']
            playlist = this.spotify.playlist(uri)
            name = playlist['name']
            if(len(playlist['name']) > 35):
              name = playlist['name'][0:35] + '...'
            else:
              name = playlist['name']
            owner = 'Playlist By: ' + playlist['owner']['display_name']

            return [name, owner]
          elif(playbackType == "album"):
            uri = this.currentSong.get('context')['uri']
            album = this.spotify.album(uri)
            name = album['name']
            if(len(album['name']) > 35):
              position = name.find('-')
              if(position != -1):
                name = name[0:position - 1]
              else:
                name = name[0:32]+'...'
            artist = 'Album By: ' + album['artists'][0]['name']
            return [name, artist]
          else:
            return ["",""]
        except:
          return ["",""]
      else:
        x = datetime.date.today()
        date = x.strftime('%A') + ", " + x.strftime('%B') + ' ' +x.strftime('%d')
        return[date,""]
    else:
      return ['Click here to choose a playlist','']

def getCurrentSong(spotify):
  data = spotify.currently_playing()
  return data
def seekPlayback(spotify, percent):
  newTime = int(spotify.currently_playing().get('item')['duration_ms'] * percent)
  playback = spotify.seek_track(newTime)
def skipPlayback(spotify):


  playback = spotify.next_track()
def previousPlayback(spotify):




  playback = spotify.previous_track()
def togglePlayback(spotify):
  playbackInfo = spotify.current_playback()
  isPlaying = playbackInfo['is_playing']
  if(isPlaying == True):
    playback = spotify.pause_playback()
    return False
  else:
    playback = spotify.start_playback()
    return True
def changeVolume(spotify, action):
  playbackInfo = spotify.current_playback()
  device = playbackInfo['device']['id']
  volume = playbackInfo['device']['volume_percent']
  if(action == "increseVolume"):
    volume += 5
    if(volume > 100):
      volume = 100
    playback = spotify.volume(volume)
  elif(action == "decreaseVolume"):
    volume -= 5
    if(volume < 0):
      volume = 0
    playback = spotify.volume(volume)
def toggleShuffle(spotify):
  playbackInfo = spotify.current_playback()
  isShuffle = playbackInfo['shuffle_state']
  if(isShuffle == True):
    playback = spotify.shuffle(False)
  else:
    playback = spotify.shuffle(True)
def toggleRepeat(spotify):
  playbackInfo = spotify.current_playback()
  isRepeat = playbackInfo['repeat_state']
  if(isRepeat == "off"):
    playback = spotify.repeat("context")
  elif(isRepeat == "context"):
    playback = spotify.repeat("track")
  elif(isRepeat == "track"):
    playback = spotify.repeat("off")
