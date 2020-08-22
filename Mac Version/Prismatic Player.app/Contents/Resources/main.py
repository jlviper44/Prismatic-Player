import tkinter as tk
import authorization
import functions
import window
import time
# authorization.auth().clearCache()
# authorization.auth().setAuth()
# authorization.auth().getToken()


spotify = authorization.auth().getToken()
if(spotify == False or spotify == None):
  spotify = authorization.auth().getToken()
# currentSong = functions.getCurrentSong(spotify)
# song1 = functions.song(spotify, currentSong)
# t = "e"
# if(int(time.strftime("%I")) < 10):
#   t = str(int(time.strftime("%I")))+time.strftime(":%M %p")
# else:
#   t = time.strftime("%I:%M %p")
# print(t)
# time.sleep(1)
try:
  window = window.create(spotify)
except:
  pass